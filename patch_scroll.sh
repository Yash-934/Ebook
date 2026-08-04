#!/bin/bash

# Find the start line for replacing the Column
START_LINE=$(grep -n "modifier =" app/src/main/java/com/example/ui/screens/ReadScreen.kt | grep -A 5 "padding(padding)" | head -n 1 | cut -d: -f1)

cat << 'INNER_EOF' > replacement.txt
                Box(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(padding)
                        .verticalScroll(scrollState)
                        .pointerInput(activeEditTool) {
                            if (activeEditTool != null) {
                                detectDragGestures(
                                    onDragStart = { offset ->
                                        val path = Path().apply { moveTo(offset.x, offset.y) }
                                        currentPath = path
                                        currentLineColor = when (activeEditTool) {
                                            "highlight" -> Color(0xFFFFD700)
                                            "underline" -> Color.Red
                                            else -> Color(0xFF87CEEB)
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
                                        currentPath?.lineTo(change.position.x, change.position.y)
                                        val newPath = Path().apply { currentPath?.let { addPath(it) } }
                                        currentPath = newPath
                                    },
                                    onDragEnd = {
                                        currentPath?.let { drawnLines.add(DrawnLine(it, currentLineColor, currentStrokeWidth, currentAlpha)) }
                                        currentPath = null
                                    },
                                    onDragCancel = { currentPath = null }
                                )
                            }
                        }
                ) {
                    Box(modifier = Modifier.fillMaxWidth()) {
                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(horizontal = margins.dp, vertical = margins.dp)
                        ) {
INNER_EOF

sed -i '/Column(/,/padding(horizontal = margins.dp, vertical = margins.dp)/c\'"$(cat replacement.txt)"'' app/src/main/java/com/example/ui/screens/ReadScreen.kt
