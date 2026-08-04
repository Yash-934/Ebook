import re

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "r") as f:
    content = f.read()

bad_pattern = r'val drawnLines = remember\(book\) \{\n\s*val list = androidx\.compose\.runtime\.mutableStateListOf<DrawnLine>\(\)\n\s*book\?\.annotations\?\.let \{ ann ->\n\s*if \(ann\.isNotEmpty\(\) && ann != "\[\]"\) \{\n\s*try \{\n\s*val array = JSONArray\(ann\)\n\s*for \(i in 0 until array\.length\(\)\) \{\n\s*val obj = array\.getJSONObject\(i\)\n\s*val colorVal = obj\.getLong\("color"\)\n\s*val strokeWidth = obj\.getDouble\("strokeWidth"\)\.toFloat\(\)\n\s*val alpha = obj\.getDouble\("alpha"\)\.toFloat\(\)\n\s*val tool = obj\.getString\("tool"\)\n\s*val pointsArray = obj\.getJSONArray\("points"\)\n\s*val points = mutableListOf<Offset>\(\)\n\s*val path = Path\(\)\n\s*for \(j in 0 until pointsArray\.length\(\)\) \{\n\s*val pt = pointsArray\.getJSONObject\(j\)\n\s*val x = pt\.getDouble\("x"\)\.toFloat\(\)\n\s*val y = pt\.getDouble\("y"\)\.toFloat\(\)\n\s*val offset = Offset\(x, y\)\n\s*points\.add\(offset\)\n\s*if \(j == 0\) path\.moveTo\(x, y\) else path\.lineTo\(x, y\)\n\s*\}\n\s*list\.add\(DrawnLine\(points, path, Color\(colorVal\.toULong\(\)\), strokeWidth, alpha, tool\)\)\n\s*\}\n\s*\} catch \(e: Exception\) \{ e\.printStackTrace\(\) \}\n\s*\}\n\s*\}\n\s*list\n\s*\}'

new_drawnLines = """val drawnLines = remember { androidx.compose.runtime.mutableStateListOf<DrawnLine>() }
    var loadedAnnotations by remember { mutableStateOf(false) }

    LaunchedEffect(book) {
        if (!loadedAnnotations && book != null) {
            val ann = book.annotations
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
                        drawnLines.add(DrawnLine(points, path, Color(colorVal.toULong()), strokeWidth, alpha, tool))
                    }
                } catch (e: Exception) { e.printStackTrace() }
            }
            loadedAnnotations = true
        }
    }"""
content = re.sub(bad_pattern, new_drawnLines, content)

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "w") as f:
    f.write(content)
