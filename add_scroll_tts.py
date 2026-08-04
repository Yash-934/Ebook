import re

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "r") as f:
    content = f.read()

target_pattern = r'ActionButton\(\n\s*icon = Icons\.Default\.Edit,\n\s*tint = textColor,\n\s*borderColor = textColor\.copy\(alpha = 0\.2f\),\n\s*onClick = \{ showEditTools = true \}\n\s*\)'

new_buttons = """ActionButton(
                                        icon = if (isAutoScrolling) Icons.Default.Pause else Icons.Default.PlayArrow,
                                        tint = textColor,
                                        borderColor = textColor.copy(alpha = 0.2f),
                                        onClick = { 
                                            isAutoScrolling = !isAutoScrolling
                                            scope.launch { snackbarHostState.showSnackbar(if (isAutoScrolling) "Auto scroll started" else "Auto scroll stopped") }
                                        }
                                    )
                                    ActionButton(
                                        icon = if (isPlayingTTS) Icons.Default.VolumeUp else Icons.Default.VolumeOff,
                                        tint = textColor,
                                        borderColor = textColor.copy(alpha = 0.2f),
                                        onClick = { 
                                            isPlayingTTS = !isPlayingTTS
                                            scope.launch { snackbarHostState.showSnackbar(if (isPlayingTTS) "TTS started" else "TTS stopped") }
                                        }
                                    )
                                    ActionButton(
                                        icon = Icons.Default.Edit,
                                        tint = textColor,
                                        borderColor = textColor.copy(alpha = 0.2f),
                                        onClick = { showEditTools = true }
                                    )"""

content = re.sub(target_pattern, new_buttons, content)

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "w") as f:
    f.write(content)
