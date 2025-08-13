package internal

import (
	"encoding/json"
	"errors"
	"os"
	"path/filepath"
	"sync"
)

type Cache struct {
	mu      sync.RWMutex
	loaded  map[string]map[string]Resource
	loading map[string]map[string]struct{}
}

func NewCache() *Cache {
	return &Cache{
		loaded:  make(map[string]map[string]Resource),
		loading: make(map[string]map[string]struct{}),
	}
}

func (c *Cache) IsLoaded(kind, name string) bool {
	c.mu.RLock()
	defer c.mu.RUnlock()
	_, ok := c.loaded[kind][name]
	return ok
}

func (c *Cache) IsLoading(kind, name string) bool {
	c.mu.RLock()
	defer c.mu.RUnlock()
	_, ok := c.loading[kind][name]
	return ok
}

func (c *Cache) MarkLoading(kind, name string) {
	c.mu.Lock()
	defer c.mu.Unlock()
	if c.loading[kind] == nil {
		c.loading[kind] = make(map[string]struct{})
	}
	c.loading[kind][name] = struct{}{}
}

func (c *Cache) Store(kind string, res Resource) {
	c.mu.Lock()
	defer c.mu.Unlock()
	if c.loaded[kind] == nil {
		c.loaded[kind] = make(map[string]Resource)
	}
	c.loaded[kind][res.GetName()] = res
	delete(c.loading[kind], res.GetName())
}

func (c *Cache) Get(kind, name string) (Resource, bool) {
	c.mu.RLock()
	defer c.mu.RUnlock()
	res, ok := c.loaded[kind][name]
	return res, ok
}

func (c *Cache) All(kind string) []Resource {
	c.mu.RLock()
	defer c.mu.RUnlock()
	var out []Resource
	for _, r := range c.loaded[kind] {
		out = append(out, r)
	}
	return out
}

func (c *Cache) SaveToDisk(path string) error {
	c.mu.RLock()
	defer c.mu.RUnlock()

	data := make(map[string]map[string]json.RawMessage)
	for kind, items := range c.loaded {
		data[kind] = make(map[string]json.RawMessage)
		for name, res := range items {
			b, err := json.Marshal(res)
			if err != nil {
				return err
			}
			data[kind][name] = b
		}
	}

	b, err := json.MarshalIndent(data, "", "  ")
	if err != nil {
		return err
	}

	if err := os.MkdirAll(filepath.Dir(path), 0755); err != nil {
		return err
	}

	return os.WriteFile(path, b, 0644)
}

func (c *Cache) LoadFromDisk(path string, factories map[string]func() Resource) error {
	c.mu.Lock()
	defer c.mu.Unlock()

	b, err := os.ReadFile(path)
	if err != nil {
		if errors.Is(err, os.ErrNotExist) {
			return nil
		}
		return err
	}

	var raw map[string]map[string]json.RawMessage
	if err := json.Unmarshal(b, &raw); err != nil {
		return err
	}

	for kind, items := range raw {
		factory, ok := factories[kind]
		if !ok {
			continue
		}
		if c.loaded[kind] == nil {
			c.loaded[kind] = make(map[string]Resource)
		}
		for name, blob := range items {
			res := factory()
			if err := json.Unmarshal(blob, res); err != nil {
				return err
			}
			c.loaded[kind][name] = res
		}
	}

	return nil
}
