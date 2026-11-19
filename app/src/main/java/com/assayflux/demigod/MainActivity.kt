package com.assayflux.demigod

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.selection.SelectionContainer
import androidx.compose.material3.Divider
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent { DemiGodTheme { DemiGodApp() } }
    }
}

private enum class WorkspaceTab(val label: String, val glyph: String) {
    CHAT("Chat", "✦"), FILES("Files", "▤"), TERMINAL("Terminal", ">_")
}

private data class ChatMessage(val id: Long, val fromUser: Boolean, val text: String)

internal data class MessageSegment(
    val text: String,
    val language: String? = null,
    val isCode: Boolean = false
)

internal fun parseMessageSegments(content: String): List<MessageSegment> {
    val fence = Regex("```([\\w+#.-]*)[ \\t]*\\n([\\s\\S]*?)```")
    val result = mutableListOf<MessageSegment>()
    var cursor = 0
    fence.findAll(content).forEach { match ->
        if (match.range.first > cursor) {
            result += MessageSegment(content.substring(cursor, match.range.first))
        }
        result += MessageSegment(
            text = match.groupValues[2].trimEnd(),
            language = match.groupValues[1].ifBlank { null },
            isCode = true
        )
        cursor = match.range.last + 1
    }
    if (cursor < content.length) result += MessageSegment(content.substring(cursor))
    if (result.isEmpty()) result += MessageSegment(content)
    return result
}

@Composable
private fun DemiGodTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = darkColorScheme(
            primary = Color(0xFFB9A5FF),
            secondary = Color(0xFF8BD5CA),
            background = Color(0xFF101116),
            surface = Color(0xFF191B22),
            surfaceVariant = Color(0xFF252832),
            onBackground = Color(0xFFF1F0F6),
            onSurface = Color(0xFFF1F0F6)
        ),
        content = content
    )
}

@Composable
private fun DemiGodApp() {
    var selectedTab by remember { mutableStateOf(WorkspaceTab.CHAT) }
    var prompt by remember { mutableStateOf("") }
    val messages = remember {
        mutableStateListOf(
            ChatMessage(
                1L,
                false,
                "Welcome to DemiGod. Your coding workspace is ready.\n\nThe chat interface is running in preview mode: no language model or command executor is connected yet. Connect a verified local model or an explicitly enabled host provider to generate real answers."
            )
        )
    }

    Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
        Column(modifier = Modifier.fillMaxSize()) {
            TopBar()
            when (selectedTab) {
                WorkspaceTab.CHAT -> ChatWorkspace(
                    modifier = Modifier.weight(1f),
                    messages = messages,
                    prompt = prompt,
                    onPromptChange = { prompt = it },
                    onSend = {
                        val value = prompt.trim()
                        if (value.isNotEmpty()) {
                            messages.add(ChatMessage(System.nanoTime(), true, value))
                            messages.add(
                                ChatMessage(
                                    System.nanoTime() + 1,
                                    false,
                                    "I received your request. A model provider is not connected in this build yet, so I have not generated code or run any commands. The next integration is the verified local-runtime / AirLLM host adapter."
                                )
                            )
                            prompt = ""
                        }
                    }
                )
                WorkspaceTab.FILES -> FilesWorkspace(Modifier.weight(1f))
                WorkspaceTab.TERMINAL -> TerminalWorkspace(Modifier.weight(1f))
            }
            NavigationBar(containerColor = MaterialTheme.colorScheme.surface) {
                WorkspaceTab.entries.forEach { tab ->
                    NavigationBarItem(
                        selected = selectedTab == tab,
                        onClick = { selectedTab = tab },
                        icon = { Text(tab.glyph, fontSize = 18.sp, fontWeight = FontWeight.Bold) },
                        label = { Text(tab.label) }
                    )
                }
            }
        }
    }
}

@Composable
private fun TopBar() {
    Row(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 18.dp, vertical = 14.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text("✦", color = MaterialTheme.colorScheme.primary, fontSize = 25.sp)
        Text(
            "  DemiGod",
            fontSize = 20.sp,
            fontWeight = FontWeight.SemiBold,
            color = MaterialTheme.colorScheme.onBackground
        )
        Spacer(Modifier.weight(1f))
        Surface(color = Color(0xFF26382F), shape = RoundedCornerShape(50)) {
            Text(
                "G54 target",
                color = Color(0xFF9FE0B5),
                fontSize = 11.sp,
                modifier = Modifier.padding(horizontal = 11.dp, vertical = 6.dp)
            )
        }
    }
    Divider(color = Color(0xFF292C35))
}

@Composable
private fun ChatWorkspace(
    modifier: Modifier = Modifier,
    messages: List<ChatMessage>,
    prompt: String,
    onPromptChange: (String) -> Unit,
    onSend: () -> Unit
) {
    Column(modifier = modifier.fillMaxWidth()) {
        LazyColumn(
            modifier = Modifier.weight(1f).fillMaxWidth(),
            contentPadding = androidx.compose.foundation.layout.PaddingValues(16.dp),
            verticalArrangement = Arrangement.spacedBy(14.dp)
        ) {
            items(messages, key = { it.id }) { message -> MessageBubble(message) }
        }
        Surface(color = MaterialTheme.colorScheme.surface, tonalElevation = 2.dp) {
            Column(modifier = Modifier.fillMaxWidth().padding(12.dp)) {
                Row(
                    modifier = Modifier.fillMaxWidth()
                        .background(MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(22.dp))
                        .padding(horizontal = 15.dp, vertical = 12.dp),
                    verticalAlignment = Alignment.Bottom
                ) {
                    BasicTextField(
                        value = prompt,
                        onValueChange = onPromptChange,
                        modifier = Modifier.weight(1f),
                        textStyle = MaterialTheme.typography.bodyLarge.copy(color = MaterialTheme.colorScheme.onSurface),
                        decorationBox = { inner ->
                            Box {
                                if (prompt.isEmpty()) {
                                    Text("Ask DemiGod to build something...", color = Color(0xFF858A98))
                                }
                                inner()
                            }
                        },
                        maxLines = 5
                    )
                    IconButton(onClick = onSend, modifier = Modifier.size(38.dp)) {
                        Text("↑", color = MaterialTheme.colorScheme.primary, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                    }
                }
                Spacer(Modifier.height(7.dp))
                Text(
                    "Model not connected · Preview mode",
                    color = Color(0xFF858A98),
                    fontSize = 10.sp
                )
            }
        }
    }
}

@Composable
private fun MessageBubble(message: ChatMessage) {
    Column(
        modifier = Modifier.fillMaxWidth(),
        horizontalAlignment = if (message.fromUser) Alignment.End else Alignment.Start
    ) {
        Text(
            if (message.fromUser) "YOU" else "DEMIGOD",
            color = Color(0xFF969BAA),
            fontSize = 10.sp,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.padding(horizontal = 5.dp, vertical = 4.dp)
        )
        Surface(
            color = if (message.fromUser) Color(0xFF343044) else MaterialTheme.colorScheme.surface,
            shape = RoundedCornerShape(18.dp),
            modifier = Modifier.fillMaxWidth(if (message.fromUser) 0.88f else 1f)
        ) {
            Column(modifier = Modifier.padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                parseMessageSegments(message.text).forEach { segment ->
                    if (segment.isCode) {
                        CodeBlockCard(segment)
                    } else if (segment.text.isNotBlank()) {
                        SelectionContainer {
                            Text(
                                segment.text,
                                color = MaterialTheme.colorScheme.onSurface,
                                fontSize = 14.sp,
                                lineHeight = 21.sp
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun CodeBlockCard(segment: MessageSegment) {
    val clipboard = LocalClipboardManager.current
    Surface(color = Color(0xFF0C0E13), shape = RoundedCornerShape(12.dp)) {
        Column(modifier = Modifier.fillMaxWidth().padding(10.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    segment.language?.uppercase() ?: "CODE",
                    color = Color(0xFF9B9FB0),
                    fontSize = 10.sp,
                    fontWeight = FontWeight.Bold
                )
                Spacer(Modifier.weight(1f))
                IconButton(
                    onClick = { clipboard.setText(AnnotatedString(segment.text)) },
                    modifier = Modifier.height(30.dp)
                ) {
                    Text("Copy", color = MaterialTheme.colorScheme.primary, fontSize = 12.sp)
                }
            }
            SelectionContainer {
                Text(
                    segment.text,
                    color = Color(0xFFD8DCE8),
                    fontFamily = FontFamily.Monospace,
                    fontSize = 12.sp,
                    lineHeight = 18.sp
                )
            }
        }
    }
}

@Composable
private fun FilesWorkspace(modifier: Modifier = Modifier) {
    Column(
        modifier = modifier.fillMaxWidth().padding(24.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("▤", fontSize = 42.sp, color = MaterialTheme.colorScheme.primary)
        Spacer(Modifier.height(12.dp))
        Text("Project files", fontSize = 20.sp, fontWeight = FontWeight.SemiBold)
        Text("Primary device profile", fontWeight = FontWeight.SemiBold, modifier = Modifier.padding(top = 8.dp))
        Surface(color = MaterialTheme.colorScheme.surface, shape = RoundedCornerShape(14.dp), modifier = Modifier.fillMaxWidth().padding(top = 14.dp)) {
            Column(modifier = Modifier.padding(16.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                Text("Moto G54 5G", fontWeight = FontWeight.SemiBold)
                Text("12 GB RAM · Android 15 · 256 GB storage target", color = Color(0xFFB9A5FF), fontSize = 12.sp)
                Text("Model loading stays disabled until a runtime checks available memory and the selected model requirements.", color = Color(0xFF969BAA), fontSize = 12.sp, lineHeight = 18.sp)
            }
        }
        Text(
            "Project picker, Storage Access Framework, repository tree and editor are the next workspace milestone.",
            color = Color(0xFF969BAA), modifier = Modifier.padding(top = 14.dp), lineHeight = 21.sp
        )
    }
}

@Composable
private fun TerminalWorkspace(modifier: Modifier = Modifier) {
    Column(modifier = modifier.fillMaxWidth().padding(16.dp)) {
        Text("Terminal", fontSize = 20.sp, fontWeight = FontWeight.SemiBold)
        Text("Command execution is intentionally disabled in this preview.", color = Color(0xFF969BAA), fontSize = 12.sp)
        Spacer(Modifier.height(14.dp))
        Surface(
            modifier = Modifier.fillMaxWidth().weight(1f),
            color = Color(0xFF090B0F),
            shape = RoundedCornerShape(14.dp)
        ) {
            Column(modifier = Modifier.padding(14.dp)) {
                Text("DemiGod isolated workspace", color = Color(0xFF9FE0B5), fontFamily = FontFamily.Monospace)
                Spacer(Modifier.height(8.dp))
                Text("runner: not configured", color = Color(0xFFE4C27A), fontFamily = FontFamily.Monospace, fontSize = 12.sp)
                Text("status: safe preview (no commands executed)", color = Color(0xFF9AA1B1), fontFamily = FontFamily.Monospace, fontSize = 12.sp)
            }
        }
        Spacer(Modifier.height(12.dp))
        Text("A permissioned, isolated command runner will be added after workspace and execution-sandbox design.", color = Color(0xFF969BAA), fontSize = 12.sp)
    }
}
