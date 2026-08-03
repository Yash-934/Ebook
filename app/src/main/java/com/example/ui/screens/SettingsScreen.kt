package com.example.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CloudSync
import androidx.compose.material.icons.filled.DarkMode
import androidx.compose.material.icons.filled.FontDownload
import androidx.compose.material.icons.filled.LightMode
import androidx.compose.material.icons.filled.SyncDisabled
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.example.ui.SettingsViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    viewModel: SettingsViewModel
) {
    val darkMode by viewModel.darkModeEnabled.collectAsState()
    val cloudSync by viewModel.cloudSyncEnabled.collectAsState()
    val fontSize by viewModel.fontSize.collectAsState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Settings") },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface,
                    titleContentColor = MaterialTheme.colorScheme.onSurface
                )
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 16.dp)
        ) {
            SettingsItem(
                title = "Dark Mode",
                description = "Enable dark theme for comfortable reading at night.",
                icon = if (darkMode) Icons.Default.DarkMode else Icons.Default.LightMode
            ) {
                Switch(checked = darkMode, onCheckedChange = { viewModel.toggleDarkMode(it) })
            }
            
            HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
            
            SettingsItem(
                title = "Cross-Device Sync",
                description = "Sync your books and reading progress across devices.",
                icon = if (cloudSync) Icons.Default.CloudSync else Icons.Default.SyncDisabled
            ) {
                Switch(checked = cloudSync, onCheckedChange = { viewModel.toggleCloudSync(it) })
            }

            HorizontalDivider(modifier = Modifier.padding(vertical = 8.dp))
            
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 12.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Icon(Icons.Default.FontDownload, contentDescription = "Font Size", modifier = Modifier.size(32.dp), tint = MaterialTheme.colorScheme.primary)
                Spacer(modifier = Modifier.width(16.dp))
                Column(modifier = Modifier.weight(1f)) {
                    Text("Reading Font Size", style = MaterialTheme.typography.titleMedium)
                    Slider(
                        value = fontSize,
                        onValueChange = { viewModel.setFontSize(it) },
                        valueRange = 12f..32f,
                        steps = 20
                    )
                }
            }
        }
    }
}

@Composable
fun SettingsItem(
    title: String,
    description: String,
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    control: @Composable () -> Unit
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(icon, contentDescription = title, modifier = Modifier.size(32.dp), tint = MaterialTheme.colorScheme.primary)
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(title, style = MaterialTheme.typography.titleMedium)
            Text(description, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
        }
        control()
    }
}
