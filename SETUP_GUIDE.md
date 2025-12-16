# 🚀 Quick Setup Guide

## Getting Your ChatGPT-like App Running

### Step 1: Install Dependencies
```bash
flutter pub get
```

### Step 2: Generate Hive Type Adapters
```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

### Step 3: Configure Environment
Create a `.env` file in the project root:
```env
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your_project_id_here
API_ENDPOINT=http://localhost:8000
```

### Step 4: Start Backend (In PowerShell)
```powershell
cd backend
.\start_backend.ps1
```

Wait for "Uvicorn running on http://0.0.0.0:8000"

### Step 5: Run the App
```bash
flutter run
```

## 🎯 What You Get

Your app now has all the features of ChatGPT/Gemini:

✅ **Multiple Conversations** - Create unlimited chat sessions  
✅ **Smart Auto-Titles** - Conversations titled from first message  
✅ **Conversation Search** - Find any chat instantly  
✅ **Markdown Support** - Beautiful formatted text and code  
✅ **Code Highlighting** - Syntax highlighting for code blocks  
✅ **Voice Input** - Speech-to-text for hands-free chatting  
✅ **Dark/Light Theme** - Toggle themes with saved preference  
✅ **Streaming Responses** - Real-time typing animation  
✅ **Export Chats** - Save conversations as JSON  
✅ **Copy Messages** - One-click copy to clipboard  
✅ **Conversation Management** - Rename, delete, clear chats  
✅ **Settings Screen** - Customize model and preferences  
✅ **Statistics** - View your chat history stats  
✅ **Responsive Design** - Works on all screen sizes  
✅ **Local Storage** - All data saved with Hive  
✅ **User Authentication** - Appwrite integration  

## 📱 Using the App

### Chat Interface
- **New Chat**: Tap menu (☰) → "New Chat"
- **Send Message**: Type and tap send, or use voice input
- **Voice Input**: Hold microphone button, speak, release
- **Copy Message**: Tap copy icon next to any message
- **Switch Chat**: Tap menu (☰) → Select conversation

### Conversation Management
- **Search**: Use search bar in drawer
- **Rename**: Tap ⋮ on conversation → Rename
- **Delete**: Tap ⋮ on conversation → Delete
- **Export**: Tap ⋮ in app bar → Export Chat

### Settings
- **Theme**: Settings → Toggle Dark Mode
- **Model**: Settings → Select AI Model
- **Stats**: Settings → View conversation statistics
- **Clear All**: Settings → Clear All Conversations

## 🔧 Troubleshooting

### Backend Won't Start
```powershell
# Check if Ollama is running
ollama list

# Restart Ollama
ollama serve
```

### App Can't Connect to Backend
1. Check backend is running on port 8000
2. Verify `.env` has correct API_ENDPOINT
3. On Android emulator, use `http://10.0.2.2:8000`
4. On iOS simulator, use `http://localhost:8000`

### Voice Input Not Working
1. Grant microphone permission in settings
2. Check device microphone works
3. Restart the app

### Hive Errors
```bash
# Regenerate type adapters
flutter pub run build_runner build --delete-conflicting-outputs
```

## 🎨 Customization

### Change App Name
Edit `pubspec.yaml`:
```yaml
name: your_app_name
```

### Change Colors
Edit `lib/main.dart` - look for `Colors.amber` and replace with your color

### Add More Models
Edit `lib/screen/settings_screen.dart` - add models to the RadioListTile list

## 📦 What Was Built

### New Files Created
```
lib/model/conversation.dart              - Conversation data models
lib/model/conversation.g.dart            - Generated Hive adapters
lib/services/conversation_service.dart   - Conversation management
lib/services/image_picker_service.dart   - Image handling
lib/controller/enhanced_chat_controller.dart - Chat logic
lib/screen/feature/new_chat_screen.dart  - Main chat UI
lib/screen/settings_screen.dart          - Settings screen
lib/widget/enhanced_message_card.dart    - Message UI with markdown
lib/widget/conversation_list_drawer.dart - Conversation drawer
```

### Enhanced Files
```
pubspec.yaml                   - Added dependencies
lib/screen/home_screen.dart   - Updated navigation
```

### New Dependencies Added
- `uuid` - Unique IDs for messages
- `intl` - Date formatting
- `hive_generator` - Generate type adapters
- `build_runner` - Code generation
- `image_picker` - Image selection
- `share_plus` - Share functionality

## 🚀 Next Steps

1. **Run the app** - See your ChatGPT-like interface!
2. **Create conversations** - Start chatting with AI
3. **Try voice input** - Hold microphone and speak
4. **Test markdown** - Ask AI to write code
5. **Customize theme** - Toggle dark mode
6. **Export chats** - Save your conversations

## 💡 Tips

- **First Run**: May take a moment to initialize Hive database
- **Voice Input**: Works best in quiet environment
- **Markdown**: Ask AI "write python code for X" to see highlighting
- **Auto-Titles**: First message becomes conversation title
- **Export**: Saves to app documents AND copies to clipboard

## 🎉 You're Ready!

Your full-featured ChatGPT/Gemini-like app is ready to use!

Enjoy chatting with AI! 🤖💬
