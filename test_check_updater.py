import updater
import json
print(json.dumps(updater.check_for_updates(), indent=2, ensure_ascii=False))
