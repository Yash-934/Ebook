package com.example.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.AutoStories
import androidx.compose.ui.draw.clip
import androidx.compose.material.icons.filled.FormatSize
import androidx.compose.material.icons.filled.Height
import androidx.compose.material.icons.filled.ImportExport
import androidx.compose.material.icons.filled.Palette
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.SpaceBar
import androidx.compose.material.icons.filled.TextFormat
import androidx.compose.material.icons.filled.ViewDay
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.example.ui.SettingsViewModel
import com.example.ui.theme.BlackThemeBackground
import com.example.ui.theme.DarkBlueThemeBackground
import com.example.ui.theme.SepiaThemeBackground
import com.example.ui.theme.WhiteThemeBackground

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsSheet(viewModel: SettingsViewModel, onDismiss: () -> Unit) {
    val themeIndex by viewModel.themeIndex.collectAsState()
    val fontFamilyIndex by viewModel.fontFamilyIndex.collectAsState()
    val fontSize by viewModel.fontSize.collectAsState()
    val lineSpacing by viewModel.lineSpacing.collectAsState()
    val wordSpacing by viewModel.wordSpacing.collectAsState()
    val margins by viewModel.margins.collectAsState()
    val scrollMode by viewModel.scrollMode.collectAsState()

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .clickable { onDismiss() }
        ) {
            Surface(
                modifier = Modifier
                    .fillMaxHeight()
                    .width(320.dp)
                    .clickable(enabled = false) {}, // Prevent dismiss when clicking inside
                color = Color(0xFFF9F5EC), // Warm beige
                shape = RoundedCornerShape(topEnd = 16.dp, bottomEnd = 16.dp)
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .verticalScroll(rememberScrollState())
                        .padding(16.dp)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.Settings, contentDescription = null, tint = Color(0xFF4FC3F7))
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("Settings", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = Color(0xFF332D28))
                        }
                        IconButton(onClick = onDismiss) {
                            Icon(Icons.Default.Close, contentDescription = "Close", tint = Color.Gray)
                        }
                    }
                    Divider(modifier = Modifier.padding(vertical = 16.dp), color = Color.LightGray)

                    // Theme
                    SectionTitle("THEME", Icons.Default.Palette)
                    Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                        ThemeCircle(WhiteThemeBackground, themeIndex == 0) { viewModel.setThemeIndex(0) }
                        ThemeCircle(DarkBlueThemeBackground, themeIndex == 1) { viewModel.setThemeIndex(1) }
                        ThemeCircle(SepiaThemeBackground, themeIndex == 2) { viewModel.setThemeIndex(2) }
                        ThemeCircle(BlackThemeBackground, themeIndex == 3) { viewModel.setThemeIndex(3) }
                    }

                    Spacer(modifier = Modifier.height(24.dp))
                    
                    // Font Family
                    SectionTitle("FONT FAMILY", Icons.Default.TextFormat)
                    OutlinedButton(onClick = { }, modifier = Modifier.fillMaxWidth(), colors = ButtonDefaults.outlinedButtonColors(contentColor = Color(0xFF332D28))) {
                        Text(if (fontFamilyIndex == 0) "Serif (Georgia)" else if (fontFamilyIndex == 1) "Sans-Serif" else "Monospace")
                    }

                    Spacer(modifier = Modifier.height(24.dp))

                    // Font Size
                    SectionTitle("FONT SIZE: ${fontSize.toInt()}PX", Icons.Default.FormatSize)
                    Slider(
                        value = fontSize,
                        onValueChange = { viewModel.setFontSize(it) },
                        valueRange = 10f..40f,
                        colors = SliderDefaults.colors(thumbColor = Color(0xFFD89E36), activeTrackColor = Color(0xFFD89E36))
                    )

                    Spacer(modifier = Modifier.height(16.dp))

                    // Line Spacing
                    SectionTitle("LINE SPACING: ${String.format("%.1f", lineSpacing)}", Icons.Default.Height)
                    Slider(
                        value = lineSpacing,
                        onValueChange = { viewModel.setLineSpacing(it) },
                        valueRange = 1.0f..3.0f,
                        colors = SliderDefaults.colors(thumbColor = Color(0xFFD89E36), activeTrackColor = Color(0xFFD89E36))
                    )

                    Spacer(modifier = Modifier.height(16.dp))

                    // Word Spacing
                    SectionTitle("WORD SPACING: ${wordSpacing.toInt()}PX", Icons.Default.SpaceBar)
                    Slider(
                        value = wordSpacing,
                        onValueChange = { viewModel.setWordSpacing(it) },
                        valueRange = 0f..20f,
                        colors = SliderDefaults.colors(thumbColor = Color(0xFFD89E36), activeTrackColor = Color(0xFFD89E36))
                    )

                    Spacer(modifier = Modifier.height(16.dp))

                    // Margins
                    SectionTitle("MARGINS: ${margins.toInt()}PX", Icons.Default.ViewDay)
                    Slider(
                        value = margins,
                        onValueChange = { viewModel.setMargins(it) },
                        valueRange = 0f..100f,
                        colors = SliderDefaults.colors(thumbColor = Color(0xFFD89E36), activeTrackColor = Color(0xFFD89E36))
                    )

                    Spacer(modifier = Modifier.height(24.dp))

                    // Reading Mode
                    SectionTitle("READING MODE", Icons.Default.AutoStories)
                    Button(
                        onClick = { viewModel.setScrollMode(!scrollMode) },
                        modifier = Modifier.fillMaxWidth(),
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFF1EAD3)),
                        shape = RoundedCornerShape(8.dp)
                    ) {
                        Text(if (scrollMode) "📜 Scroll Mode" else "📖 Paged Mode", color = Color(0xFF332D28))
                    }

                    Spacer(modifier = Modifier.height(32.dp))

                    // Data Management
                    SectionTitle("DATA MANAGEMENT", Icons.Default.ImportExport)
                    Button(onClick = {}, modifier = Modifier.fillMaxWidth(), colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFF1EAD3))) { Text("📤 Export Highlights & Progress", color = Color(0xFF332D28)) }
                    Spacer(modifier = Modifier.height(8.dp))
                    Button(onClick = {}, modifier = Modifier.fillMaxWidth(), colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFF1EAD3))) { Text("📥 Import Data", color = Color(0xFF332D28)) }
                    Spacer(modifier = Modifier.height(8.dp))
                    Button(onClick = {}, modifier = Modifier.fillMaxWidth(), colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFE53935))) { Text("🗑️ Clear Library", color = Color.White) }
                    Spacer(modifier = Modifier.height(32.dp))
                }
            }
        }
    }
}

@Composable
fun SectionTitle(title: String, icon: androidx.compose.ui.graphics.vector.ImageVector) {
    Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.padding(bottom = 8.dp)) {
        Icon(icon, contentDescription = null, tint = Color.Gray, modifier = Modifier.size(16.dp))
        Spacer(modifier = Modifier.width(8.dp))
        Text(title, fontSize = 12.sp, fontWeight = FontWeight.Bold, color = Color.Gray)
    }
}

@Composable
fun ThemeCircle(color: Color, isSelected: Boolean, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .size(40.dp)
            .clip(CircleShape)
            .background(color)
            .border(
                width = if (isSelected) 3.dp else 1.dp,
                color = if (isSelected) Color(0xFFD89E36) else Color.LightGray,
                shape = CircleShape
            )
            .clickable { onClick() }
    )
}
