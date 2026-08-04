import re

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "r") as f:
    content = f.read()

# Make sure org.json.JSONArray and JSONObject are imported
if "import org.json.JSONArray" not in content:
    content = content.replace("import com.example.ui.SettingsViewModel", "import com.example.ui.SettingsViewModel\nimport org.json.JSONArray\nimport org.json.JSONObject")
if "import androidx.compose.ui.graphics.Color" not in content:
    content = content.replace("import androidx.compose.ui.Alignment", "import androidx.compose.ui.Alignment\nimport androidx.compose.ui.graphics.Color")

# Replace drawnLines remember
drawnLines_pattern = r'val drawnLines = remember \{ androidx\.compose\.runtime\.mutableStateListOf<DrawnLine>\(\) \}'

new_drawnLines = """val drawnLines = remember(bookId) {
        val list = androidx.compose.runtime.mutableStateListOf<DrawnLine>()
        book?.annotations?.let { ann ->
            if (ann.isNotEmpty() && ann != "[]") {
                try {
                    val array = JSONArray(ann)
                    for (i in 0 until array.length()) {
                        val obj = array.getJSONObject(i)
                        val colorVal = obj.getLong("color")
                        val strokeWidth = obj.getDouble("strokeWidth").toFloat()
                        val alpha = obj.getDouble("alpha").toFloat()
                        val tool = obj.getString("tool")
                        val pointsArray = obj.getJSONArray("points")
                        val points = mutableListOf<Offset>()
                        val path = Path()
                        for (j in 0 until pointsArray.length()) {
                            val pt = pointsArray.getJSONObject(j)
                            val x = pt.getDouble("x").toFloat()
                            val y = pt.getDouble("y").toFloat()
                            val offset = Offset(x, y)
                            points.add(offset)
                            if (j == 0) path.moveTo(x, y) else path.lineTo(x, y)
                        }
                        list.add(DrawnLine(points, path, Color(colorVal.toULong()), strokeWidth, alpha, tool))
                    }
                } catch (e: Exception) { e.printStackTrace() }
            }
        }
        list
    }"""
content = re.sub(drawnLines_pattern, new_drawnLines, content)

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "w") as f:
    f.write(content)
