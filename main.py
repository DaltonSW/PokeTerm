from poketerm import main
from poketerm.utils import testing
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "cache":
        testing.handle_cache_test()
    main.main()
