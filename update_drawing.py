import re

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "r") as f:
    content = f.read()

# Make sure we import Offset
if "import androidx.compose.ui.geometry.Offset" not in content:
    content = content.replace("import androidx.compose.ui.Alignment", "import androidx.compose.ui.geometry.Offset\nimport androidx.compose.ui.Alignment")

# Update detectDragGestures
drag_pattern = r'detectDragGestures\(\n\s*onDragStart = \{ offset ->\n\s*val path = Path\(\)\.apply \{ moveTo\(offset\.x, offset\.y\) \}\n\s*currentPath = path\n\s*currentLineColor = when \(activeEditTool\) \{\n\s*"highlight" -> highlightColor\n\s*"underline" -> underlineColor\n\s*else -> doodleColor\n\s*\}\n\s*currentStrokeWidth = when \(activeEditTool\) \{\n\s*"highlight" -> 40f\n\s*"underline" -> 5f\n\s*else -> 8f\n\s*\}\n\s*currentAlpha = when \(activeEditTool\) \{\n\s*"highlight" -> 0\.4f\n\s*else -> 0\.8f\n\s*\}\n\s*\},\n\s*onDrag = \{ change, dragAmount ->\n\s*change\.consume\(\)\n\s*currentPath\?\.lineTo\(change\.position\.x, change\.position\.y\)\n\s*val newPath = Path\(\)\.apply \{ currentPath\?\.let \{ addPath\(it\) \} \}\n\s*currentPath = newPath\n\s*\},\n\s*onDragEnd = \{\n\s*currentPath\?\.let \{ drawnLines\.add\(DrawnLine\(it, currentLineColor, currentStrokeWidth, currentAlpha\)\) \}\n\s*currentPath = null\n\s*\},\n\s*onDragCancel = \{ currentPath = null \}\n\s*\)'

new_drag = """var currentPoints = mutableListOf<Offset>()
                            detectDragGestures(
                                onDragStart = { offset ->
                                    currentPoints = mutableListOf(offset)
                                    val path = Path().apply { moveTo(offset.x, offset.y) }
                                    currentPath = path
                                    currentLineColor = when (activeEditTool) {
                                        "highlight" -> highlightColor
                                        "underline" -> underlineColor
                                        else -> doodleColor
                                    }
                                    currentStrokeWidth = when (activeEditTool) {
                                        "highlight" -> 40f
                                        "underline" -> 5f
                                        else -> 8f
                                    }
                                    currentAlpha = when (activeEditTool) {
                                        "highlight" -> 0.4f
                                        else -> 0.8f
                                    }
                                },
                                onDrag = { change, dragAmount ->
                                    change.consume()
                                    currentPoints.add(change.position)
                                    currentPath?.lineTo(change.position.x, change.position.y)
                                    val newPath = Path().apply { currentPath?.let { addPath(it) } }
                                    currentPath = newPath
                                },
                                onDragEnd = {
                                    currentPath?.let { 
                                        drawnLines.add(DrawnLine(currentPoints.toList(), it, currentLineColor, currentStrokeWidth, currentAlpha, activeEditTool ?: "doodle"))
                                        ebookViewModel.updateAnnotations(book.id, drawnLines)
                                    }
                                    currentPath = null
                                },
                                onDragCancel = { currentPath = null }
                            )"""

content = re.sub(drag_pattern, new_drag, content)
with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "w") as f:
    f.write(content)
