package internal

import (
	"sort"
	"sync"
)

// Cache stores maps of currently loaded Resources, Resources
// currently being loaded, and ResourceRefs for fuzzy searching
type Cache struct {
	mu sync.RWMutex

	loaded  map[ResKind]map[string]Resource
	loading map[ResKind]map[string]struct{}

	refs map[ResKind]map[string]ResourceRef
}

// Creates a new cache
func NewCache() *Cache {
	return &Cache{
		loaded:  make(map[ResKind]map[string]Resource),
		loading: make(map[ResKind]map[string]struct{}),
		refs:    make(map[ResKind]map[string]ResourceRef),
	}
}

func (c *Cache) RegisterRef(ref ResourceRef) {
	c.mu.Lock()
	defer c.mu.Unlock()
	if c.refs[ref.Kind] == nil {
		c.refs[ref.Kind] = make(map[string]ResourceRef)
	}
	c.refs[ref.Kind][ref.Name] = ref
}

func (c *Cache) AllRefs() []ResourceRef {
	c.mu.RLock()
	defer c.mu.RUnlock()
	var out []ResourceRef
	for _, kindRefs := range c.refs {
		for _, r := range kindRefs {
			out = append(out, r)
		}
	}
	sort.Slice(out, func(i, j int) bool {
		return out[i].Name < out[j].Name
	})
	return out
}

// Checks if a resource is already loaded
func (c *Cache) IsLoaded(kind ResKind, name string) bool {
	c.mu.RLock()
	defer c.mu.RUnlock()
	_, ok := c.loaded[kind][name]
	return ok
}

// Checks if a resouce is currently being loaded in another thread
func (c *Cache) IsLoading(kind ResKind, name string) bool {
	c.mu.RLock()
	defer c.mu.RUnlock()
	_, ok := c.loading[kind][name]
	return ok
}

// Marks a resource as currently being loaded
func (c *Cache) MarkLoading(kind ResKind, name string) {
	c.mu.Lock()
	defer c.mu.Unlock()
	if c.loading[kind] == nil {
		c.loading[kind] = make(map[string]struct{})
	}
	c.loading[kind][name] = struct{}{}
}

// Store a resource in the cache map
func (c *Cache) Store(kind ResKind, res Resource) {
	c.mu.Lock()
	defer c.mu.Unlock()
	if c.loaded[kind] == nil {
		c.loaded[kind] = make(map[string]Resource)
	}
	c.loaded[kind][res.GetName()] = res
	delete(c.loading[kind], res.GetName())
}

// Get a resource from the cache map
func (c *Cache) Get(kind ResKind, name string) (Resource, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()
	res, ok := c.loaded[kind][name]
	return res, ok
}

// Get all resources of a certain kind from the cache
func (c *Cache) All(kind ResKind) []Resource {
	c.mu.RLock()
	defer c.mu.RUnlock()
	var out []Resource
	for _, r := range c.loaded[kind] {
		out = append(out, r)
	}
	return out
}

// TODO: Implement disk caching

// func (c *Cache) SaveToDisk(path string) error {
// 	c.mu.RLock()
// 	defer c.mu.RUnlock()
//
// 	data := make(map[ResKind]map[string]json.RawMessage)
// 	for kind, items := range c.loaded {
// 		data[kind] = make(map[string]json.RawMessage)
// 		for name, res := range items {
// 			b, err := json.Marshal(res)
// 			if err != nil {
// 				return err
// 			}
// 			data[kind][name] = b
// 		}
// 	}
//
// 	b, err := json.MarshalIndent(data, "", "  ")
// 	if err != nil {
// 		return err
// 	}
//
// 	if err := os.MkdirAll(filepath.Dir(path), 0755); err != nil {
// 		return err
// 	}
//
// 	return os.WriteFile(path, b, 0644)
// }
//
// func (c *Cache) LoadFromDisk(path string, factories map[ResKind]func() Resource) error {
// 	c.mu.Lock()
// 	defer c.mu.Unlock()
//
// 	b, err := os.ReadFile(path)
// 	if err != nil {
// 		if errors.Is(err, os.ErrNotExist) {
// 			return nil
// 		}
// 		return err
// 	}
//
// 	var raw map[ResKind]map[string]json.RawMessage
// 	if err := json.Unmarshal(b, &raw); err != nil {
// 		return err
// 	}
//
// 	for kind, items := range raw {
// 		factory, ok := factories[kind]
// 		if !ok {
// 			continue
// 		}
// 		if c.loaded[kind] == nil {
// 			c.loaded[kind] = make(map[string]Resource)
// 		}
// 		for name, blob := range items {
// 			res := factory()
// 			if err := json.Unmarshal(blob, res); err != nil {
// 				return err
// 			}
// 			c.loaded[kind][name] = res
// 		}
// 	}
//
// 	return nil
// }
