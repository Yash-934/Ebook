with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

import re
match = re.search(r'@OptIn\(ExperimentalFoundationApi::class\)\n@Composable\nfun BookItem\(.*?\n}\n', content, flags=re.DOTALL)
if match:
    print(match.group(0))
