import re

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "r") as f:
    content = f.read()

if "import androidx.compose.foundation.gestures.detectTapGestures" not in content:
    content = content.replace("import androidx.compose.foundation.gestures.detectDragGestures", "import androidx.compose.foundation.gestures.detectDragGestures\nimport androidx.compose.foundation.gestures.detectTapGestures")

canvas_pattern = r'Canvas\(modifier = Modifier\.matchParentSize\(\)\) \{'

new_canvas = """Canvas(modifier = Modifier
                        .matchParentSize()
                        .pointerInput(Unit) {
                            detectTapGestures(
                                onLongPress = { offset ->
                                    // Find closest line and remove it
                                    val threshold = 40f
                                    val lineToRemove = drawnLines.find { line ->
                                        line.points.any { pt ->
                                            val dx = pt.x - offset.x
                                            val dy = pt.y - offset.y
                                            (dx * dx + dy * dy) < threshold * threshold
                                        }
                                    }
                                    if (lineToRemove != null) {
                                        drawnLines.remove(lineToRemove)
                                        ebookViewModel.updateAnnotations(bookId, drawnLines)
                                    }
                                }
                            )
                        }
                    ) {"""

content = re.sub(canvas_pattern, new_canvas, content)

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "w") as f:
    f.write(content)
