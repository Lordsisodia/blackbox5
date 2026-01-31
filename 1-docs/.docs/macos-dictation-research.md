# macOS Dictation Apps: Custom System Prompt Research

**Date:** January 31, 2026
**Purpose:** Research macOS dictation services with editable system prompts, and cost analysis for building a custom solution.

---

## Executive Summary

There are several excellent macOS dictation apps that support custom system prompts. The best options are **MacWhisper Pro** (most flexible), **Superwhisper** (best UX), and **BoltAI** (most powerful). Building your own is technically feasible for ~$0/month using on-device Whisper models, requiring approximately 8-16 hours of development time.

---

## Part 1: Existing Solutions with Custom Prompts

### 1. MacWhisper (Recommended for Flexibility)

**Custom Prompt Features:**
- ✅ **Fully editable AI prompts** for dictation in Settings > Dictation
- ✅ **App-specific prompts**: Different prompts per application (e.g., professional tone for email, casual for chat)
- ✅ Integration with ChatGPT, Claude, and other AI services for post-processing
- ✅ Create unlimited custom workflows (auto-clean, translate, expand, format)

**Pricing:**
- Free version: Basic transcription
- Pro: €29-59 one-time purchase
- Requires: Your own OpenAI API key for AI features

**Best For:** Users who want deep customization and don't mind technical setup.

**Sources:**
- [MacWhisper App-Specific Dictation Prompts](https://macwhisper.helpscoutdocs.com/article/31-app-specific-dictation-prompts)
- [MacWhisper Dictation Feature](https://macwhisper.helpscoutdocs.com/article/14-how-to-use-the-dictation-feature)

---

### 2. Superwhisper (Recommended for Ease of Use)

**Custom Prompt Features:**
- ✅ **"Modes" system** — editable presets that act as system prompts
- ✅ Context-aware transcription using screen/clipboard content
- ✅ Custom vocabulary and terminology support
- ✅ Alfred workflow integration for advanced users

**Pricing:**
- Free plan: Includes basic prompt customization
- Pro: ~$8.49/month

**Best For:** Users who want good customization without technical complexity.

**Sources:**
- [Superwhisper Review and Alternatives](https://skywork.ai/skypage/en/Superwhisper-Review-The-AI-Dictation-Tool-That-Actually-Understands-You/1976166416821317632)
- [Superwhisper vs MacWhisper Comparison](https://whisperclip.com/blog/posts/whisperclip-vs-superwhisper-wisprflow-macwhisper-which-ai-dictation-fits-your-workflow)

---

### 3. BoltAI (Recommended for Power Users)

**Custom Prompt Features:**
- ✅ **Full system prompt customization** + "AI Agents" with custom instructions
- ✅ 300+ models (OpenAI, Anthropic, Google, local via Ollama/LM Studio)
- ✅ Advanced LLM parameters (temperature, tokens, etc.)
- ✅ "Instant Dictation" works in any text field

**Pricing:**
- $37/month subscription

**Best For:** Users who want maximum control over LLM behavior and local model support.

**Sources:**
- [BoltAI Features](https://help.boltai.com/articles/2306606-features)

---

### 4. Wispr Flow / VoiceInk

**Custom Prompt Features:**
- ✅ **Command Mode** — voice-controlled editing (rewrite shorter, bulletize, adjust tone)
- ✅ Tone matching across apps
- ✅ Per-app settings

**Pricing:**
- Wispr Flow: ~$12/month
- VoiceInk: Open source (free)

**Best For:** Users who want to edit text via voice commands after dictation.

---

### 5. Open Source Alternatives

| Project | Custom Prompts | Platform | Cost |
|---------|---------------|----------|------|
| **Tambourine Voice** | ✅ Yes | macOS/Win/Linux | Free |
| **macos-dictate** | ✅ Yes | macOS | Free |
| **OpenWhispr** | ✅ Yes | Cross-platform | Free |
| **VoiceFlow** | ✅ Yes | macOS | Free |

**Notable:** [VoiceFlow](https://github.com/lukaj99/voiceflow-macos) is a complete, production-ready macOS dictation app with Swift 6, speech recognition, and global hotkeys.

---

## Part 2: Build Your Own — Cost Analysis

### Option A: Cloud-Based (OpenAI Whisper API)

| Aspect | Details |
|--------|---------|
| **Transcription Cost** | **$0.006/minute** ($0.36/hour) |
| **LLM Cost** | Varies by provider (~$0.01-0.10 per dictation) |
| **Monthly (1 hr/day)** | ~$10.80 + LLM costs |
| **Monthly (4 hr/day)** | ~$43.20 + LLM costs |
| **Setup Time** | 2-4 hours |
| **Privacy** | ❌ Audio sent to cloud |

**Best For:** Quick prototyping, minimal upfront investment.

---

### Option B: On-Device (WhisperKit — Recommended)

| Aspect | Details |
|--------|---------|
| **Transcription Cost** | **$0** (runs on Apple Silicon Neural Engine) |
| **LLM Cost** | $0 if using local models (Ollama/LM Studio) |
| **Monthly Cost** | **$0** |
| **Setup Time** | 8-16 hours |
| **Privacy** | ✅ 100% on-device |
| **Requirements** | Apple Silicon Mac (M1/M2/M3/M4) |

**Best For:** Privacy-focused users, no ongoing costs, works offline.

**Technical Stack:**
- **Framework:** [WhisperKit](https://github.com/argmaxinc/WhisperKit) (Apple Silicon optimized)
- **UI:** SwiftUI with NSPanel for floating window
- **Hotkeys:** KeyboardShortcuts library or Carbon API
- **Local LLM:** Ollama or LM Studio for prompt processing

---

### Option C: Hybrid (Groq API)

| Aspect | Details |
|--------|---------|
| **Transcription Cost** | ~$0.003/minute (faster than OpenAI) |
| **Monthly (1 hr/day)** | ~$5.40 |
| **Speed** | ~0.83s vs 1.75s (OpenAI) |
| **Setup Time** | 2-4 hours |

**Best For:** Real-time streaming, cost-conscious cloud users.

---

## Part 3: Build-Your-Own Architecture

### Core Components

```
┌─────────────────────────────────────────────────────────────┐
│                    macOS Dictation App                      │
├─────────────────────────────────────────────────────────────┤
│  1. Global Hotkey (⌘⌘ double-tap)                          │
│     └── KeyboardShortcuts library or Carbon API            │
│                                                             │
│  2. Floating Panel (NSPanel)                               │
│     └── Spotlight-style overlay, non-activating            │
│                                                             │
│  3. Audio Capture                                          │
│     └── AVAudioEngine → PCM buffer                         │
│                                                             │
│  4. Transcription Backend (choose one):                    │
│     a) WhisperKit (local, free)                            │
│     b) OpenAI Whisper API ($0.006/min)                     │
│     c) Groq API (faster, cheaper)                          │
│                                                             │
│  5. LLM Post-Processing (optional):                        │
│     a) Local (Ollama/LM Studio) — free                     │
│     b) OpenAI/Claude API — pay per use                     │
│                                                             │
│  6. Output                                                 │
│     └── Paste to clipboard or type into focused field      │
└─────────────────────────────────────────────────────────────┘
```

### Key Libraries

| Component | Library | Purpose |
|-----------|---------|---------|
| Global Hotkeys | [KeyboardShortcuts](https://github.com/sindresorhus/KeyboardShortcuts) | ⌘⌘ detection |
| Floating Panel | Custom NSPanel subclass | Spotlight-style UI |
| Local Whisper | [WhisperKit](https://github.com/argmaxinc/WhisperKit) | On-device transcription |
| Audio Recording | AVFoundation | Microphone access |
| Local LLM | Ollama.swift | Post-processing |

### Example Implementation Structure

```swift
// App entry point
@main
struct DictationApp: App {
    @StateObject private var dictationManager = DictationManager()

    var body: some Scene {
        MenuBarExtra("Dictate", systemImage: "mic.fill") {
            SettingsView()
        }
    }
}

// Core manager
class DictationManager: ObservableObject {
    // Configuration
    @AppStorage("systemPrompt") var systemPrompt: String = "Clean up this text..."
    @AppStorage("useLocalModel") var useLocalModel: Bool = true

    // Services
    private let whisperKit = WhisperKitService()
    private let llmProcessor = LLMService()

    func startDictation() {
        // 1. Show floating panel
        // 2. Start recording
        // 3. Transcribe with Whisper
        // 4. Process with LLM using custom prompt
        // 5. Type result into active field
    }
}
```

---

## Part 4: Recommendation

### If You Want Something Now

| Priority | Recommendation | Cost |
|----------|---------------|------|
| Maximum flexibility | **MacWhisper Pro** | €59 one-time + API costs |
| Best UX | **Superwhisper** | Free-$8.49/mo |
| Power user features | **BoltAI** | $37/mo |
| Free + open source | **VoiceFlow** (GitHub) | Free |

### If You Want to Build Your Own

**Estimated Costs:**
- **Development time:** 8-16 hours (Swift developer)
- **Monthly operating cost:** $0 (WhisperKit + local LLM)
- **Alternative monthly cost:** $10-45 (cloud APIs)

**Recommended Approach:**
1. Start with [VoiceFlow](https://github.com/lukaj99/voiceflow-macos) as a reference
2. Integrate WhisperKit for on-device transcription
3. Add Ollama for local LLM post-processing
4. Build a simple settings UI for editing the system prompt

**Key Resources:**
- [WhisperKit GitHub](https://github.com/argmaxinc/WhisperKit) — Apple Silicon optimized
- [VoiceFlow macOS](https://github.com/lukaj99/voiceflow-macos) — Complete working example
- [Floating Panel Tutorial](https://whid.eu/2022/06/03/chapter-6-creating-a-spotlight-like-floating-panel-in-swift/)
- [Global Hotkeys in Swift](https://www.fullstackstanley.com/articles/creating-a-global-configurable-shortcut-for-macos-apps-in-swift/)

---

## Sources

1. [MacWhisper App-Specific Dictation Prompts](https://macwhisper.helpscoutdocs.com/article/31-app-specific-dictation-prompts)
2. [MacWhisper Dictation Feature](https://macwhisper.helpscoutdocs.com/article/14-how-to-use-the-dictation-feature)
3. [Superwhisper Review](https://skywork.ai/skypage/en/Superwhisper-Review-The-AI-Dictation-Tool-That-Actually-Understands-You/1976166416821317632)
4. [WhisperClip vs Superwhisper vs Wispr Flow](https://whisperclip.com/blog/posts/whisperclip-vs-superwhisper-wisprflow-macwhisper-which-ai-dictation-fits-your-workflow)
5. [BoltAI Features](https://help.boltai.com/articles/2306606-features)
6. [Whisper API Pricing 2025](https://brasstranscripts.com/blog/openai-whisper-api-pricing-2025-self-hosted-vs-managed)
7. [WhisperKit GitHub](https://github.com/argmaxinc/WhisperKit)
8. [VoiceFlow macOS](https://github.com/lukaj99/voiceflow-macos)
9. [Floating Panel Tutorial](https://whid.eu/2022/06/03/chapter-6-creating-a-spotlight-like-floating-panel-in-swift/)
10. [Global Hotkeys in Swift](https://www.fullstackstanley.com/articles/creating-a-global-configurable-shortcut-for-macos-apps-in-swift/)
11. [Spotlight-like Hotkey Window](https://ardentswift.com/posts/hotkey-window/)
12. [Create Spotlight/Alfred Window](https://www.markusbodner.com/til/2021/02/08/create-a-spotlight/alfred-like-window-on-macos-with-swiftui/)

---

*Document created for Blackbox5 research purposes.*
