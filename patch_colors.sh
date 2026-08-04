#!/bin/bash
sed -i 's/var activeEditTool by remember { mutableStateOf<String?>(null) }/&\n    var highlightColor by remember { mutableStateOf(Color(0xFFFFD700)) }\n    var underlineColor by remember { mutableStateOf(Color.Red) }\n    var doodleColor by remember { mutableStateOf(Color(0xFF87CEEB)) }/' app/src/main/java/com/example/ui/screens/ReadScreen.kt
