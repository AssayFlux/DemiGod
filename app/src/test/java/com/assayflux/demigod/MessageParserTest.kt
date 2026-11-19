package com.assayflux.demigod

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class MessageParserTest {
    @Test
    fun parsesCodeFenceAndSurroundingText() {
        val parts = parseMessageSegments("Before\n\n```kotlin\nval answer = 42\n```\n\nAfter")
        assertEquals(3, parts.size)
        assertEquals("Before\n\n", parts[0].text)
        assertTrue(parts[1].isCode)
        assertEquals("kotlin", parts[1].language)
        assertEquals("val answer = 42", parts[1].text)
        assertEquals("\n\nAfter", parts[2].text)
    }
}
