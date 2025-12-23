# Selçuk YZ Asistan (Selcuk AI Assistant) - ChatGPT/Gemini-like Mobile App

A fully-featured AI chat assistant mobile application built with Flutter, similar to ChatGPT and Google Gemini mobile apps. This app provides an intuitive interface for conversing with AI, complete with conversation management, markdown support, voice input, and more.

## ✨ Features

### 💬 Chat Experience
- **Multiple Conversations**: Create, manage, and switch between multiple chat conversations
- **Smart Titles**: Auto-generated conversation titles from first message
- **Message History**: All conversations are saved locally with Hive database
- **Streaming Responses**: Real-time typing animation for AI responses
- **Markdown Support**: Full markdown rendering with code syntax highlighting
- **Copy to Clipboard**: Easy copy functionality for messages and code blocks

### 🎨 User Interface
- **Modern Design**: Clean, intuitive interface inspired by ChatGPT and Gemini
- **Dark/Light Mode**: Toggle between themes with persistent preference
- **Conversation Drawer**: Slide-out menu showing all your chats
- **Search Conversations**: Quickly find past conversations
- **Suggested Prompts**: Quick-start prompts on empty chat screen
- **Smooth Animations**: Polished transitions and animations throughout

### 🔧 Functionality
- **Voice Input**: Speech-to-text for hands-free messaging
- **Export Conversations**: Save chats as JSON files
- **Conversation Management**: Rename, delete, or clear conversations
- **Settings Screen**: Customize model, theme, and preferences
- **Statistics**: View total conversations and message counts
- **Authentication**: Appwrite integration for user management

### 🛠 Technical Features
- **Local Database**: Hive for fast, local data persistence
- **State Management**: GetX for reactive state management
- **Backend Integration**: RESTful API integration with Ollama backend
- **Type-Safe Models**: Strongly typed data models with Hive adapters
- **Error Handling**: Comprehensive error handling and user feedback
- **Responsive Design**: Adapts to different screen sizes

## 📱 Screenshots

The app features:
- **Chat Screen**: Main conversation interface with message bubbles
- **Drawer Menu**: List of all conversations with search
- **Settings**: Comprehensive settings and preferences
- **Voice Input**: Visual feedback for voice recording
- **Markdown Rendering**: Beautiful code blocks and formatted text

## 🚀 Getting Started

### Prerequisites
- Flutter SDK (>=3.4.3 <4.0.0)
- Dart SDK
- Ollama backend running (see backend setup)
- Android/iOS development environment

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd SelcukAiAssistant
   ```

2. **Install dependencies**
   ```bash
   flutter pub get
   ```

3. **Generate Hive adapters**
   ```bash
   flutter pub run build_runner build --delete-conflicting-outputs
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   APPWRITE_ENDPOINT=your_appwrite_endpoint
   APPWRITE_PROJECT_ID=your_project_id
   API_ENDPOINT=http://your-backend:8000
   ```

5. **Run the app**
   ```bash
   flutter run
   ```

## 🔧 Backend Setup

The app requires a backend server running Ollama. See the `backend/` directory for:
- Python FastAPI server
- Ollama integration
- DeepSeek model setup
- Start scripts

To start the backend:
```powershell
cd backend
.\start_backend.ps1
```

## 📦 Dependencies

### Main Dependencies
- `flutter`: UI framework
- `get`: State management and navigation
- `hive`: Local NoSQL database
- `hive_flutter`: Flutter bindings for Hive
- `http`: HTTP client for API calls
- `flutter_markdown_plus`: Markdown rendering
- `speech_to_text`: Voice input
- `uuid`: Unique ID generation
- `intl`: Internationalization and date formatting
- `image_picker`: Image selection (prepared for future multimodal support)
- `share_plus`: Share functionality
- `appwrite`: Backend as a service
- `lottie`: Animations
- `flutter_animate`: UI animations

### Dev Dependencies
- `build_runner`: Code generation
- `hive_generator`: Generate Hive type adapters
- `flutter_lints`: Linting rules
- `very_good_analysis`: Additional analysis

## 📂 Project Structure

```
lib/
├── apis/                    # API integration
│   ├── apis.dart           # Main API calls
│   └── app_write.dart      # Appwrite configuration
├── controller/             # GetX controllers
│   ├── chat_controller.dart          # Original chat controller
│   └── enhanced_chat_controller.dart # New enhanced controller
├── helper/                 # Helper classes
│   ├── global.dart        # Global constants
│   ├── pref.dart          # Shared preferences
│   ├── my_dialog.dart     # Dialog utilities
│   └── ad_helper.dart     # Ad integration
├── model/                  # Data models
│   ├── conversation.dart   # Conversation and message models
│   ├── conversation.g.dart # Generated Hive adapters
│   ├── message.dart        # Legacy message model
│   ├── onboard.dart       # Onboarding model
│   └── home_type.dart     # Home screen types
├── screen/                 # UI screens
│   ├── splash_screen.dart
│   ├── onboarding_screen.dart
│   ├── home_screen.dart
│   ├── settings_screen.dart
│   ├── auth/
│   │   ├── login_screen.dart
│   │   └── register_screen.dart
│   └── feature/
│       ├── chatbot_feature.dart    # Original chat screen
│       └── new_chat_screen.dart    # Enhanced chat screen
├── services/               # Business logic services
│   ├── appwrite_service.dart
│   ├── conversation_service.dart   # Conversation management
│   ├── voice_service.dart
│   └── image_picker_service.dart
├── widget/                 # Reusable widgets
│   ├── message_card.dart           # Original message UI
│   ├── enhanced_message_card.dart  # New message UI with markdown
│   └── conversation_list_drawer.dart # Conversation drawer
└── main.dart              # App entry point
```

## 🎯 Usage

### Creating a Conversation
1. Open the app
2. Tap the menu icon (☰) to open the drawer
3. Tap "New Chat"
4. Start typing or use voice input

### Managing Conversations
- **Rename**: Tap the ⋮ menu on any conversation → Rename
- **Delete**: Tap the ⋮ menu → Delete
- **Search**: Use the search bar in the drawer
- **Switch**: Tap any conversation to open it

### Using Voice Input
1. Tap and hold the microphone icon
2. Speak your message
3. Release to stop recording
4. The text will appear in the input field
5. Tap send

### Copying Messages
- Tap the copy icon next to any message
- For code blocks, use the copy button in the code block header

### Exporting Conversations
1. Open the conversation
2. Tap the ⋮ menu in the app bar
3. Select "Export Chat"
4. The conversation is saved and copied to clipboard

## 🔐 Authentication

The app uses Appwrite for authentication:
- **Login**: Email and password
- **Register**: Create new account
- **Session Management**: Automatic session handling
- **Logout**: Secure logout from all devices

## 🎨 Customization

### Changing Theme
1. Go to Settings (⚙️ icon in drawer)
2. Toggle "Dark Mode"
3. Preference is saved automatically

### Selecting AI Model
1. Open Settings
2. Tap on "Model"
3. Select from available models:
   - DeepSeek R1 Distill (faster)
   - DeepSeek R1 (more capable)

## 🐛 Troubleshooting

### Backend Connection Issues
- Ensure backend server is running
- Check `.env` file has correct API endpoint
- Verify network connectivity
- Check backend logs for errors

### Voice Input Not Working
- Grant microphone permissions
- Check device microphone is working
- Try restarting the app

### Messages Not Saving
- Check storage permissions
- Clear app data and try again
- Ensure Hive initialization succeeded

## 📝 Development Notes

### Adding New Features
1. Create models in `lib/model/`
2. Add services in `lib/services/`
3. Create controllers in `lib/controller/`
4. Build UI in `lib/screen/` or `lib/widget/`
5. Update dependencies in `pubspec.yaml`

### Running Tests
```bash
flutter test
```

### Building for Production
```bash
# Android
flutter build apk --release

# iOS
flutter build ios --release
```

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- OpenAI ChatGPT for inspiration
- Google Gemini for UI/UX inspiration
- Flutter team for amazing framework
- Ollama for local AI inference
- DeepSeek for the AI models

## 📧 Contact

For questions or support, please contact the development team.

---

**Built with ❤️ using Flutter and AI**
