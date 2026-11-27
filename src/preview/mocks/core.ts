/** Stand-in for @tauri-apps/api/core so the UI can render without a Tauri shell. */

const settings = {
  always_on_microphone: false,
  selected_microphone: "Default",
  clamshell_microphone: "Default",
  selected_output_device: "Default",
  audio_feedback: true,
  audio_feedback_volume: 0.5,
  sound_theme: "custom",
  start_hidden: true,
  close_button: "hide",
  autostart_enabled: true,
  update_checks_enabled: false,
  show_whats_new_on_update: false,
  whats_new_last_seen_version: "0.10.2",
  shortcut_activation: "hold_or_toggle",
  hold_threshold_ms: 200,
  spoken_languages: ["en", "ru"],
  translate_to_english: false,
  selected_language: "auto",
  chinese_script: "simplified",
  overlay_position: "bottom",
  overlay_style: "live",
  debug_mode: false,
  experimental_enabled: false,
  custom_words: ["Voxa", "Linear"],
  word_correction_threshold: 0.18,
  paste_delay_ms: 0,
  paste_delay_after_ms: 0,
  reliable_paste: true,
  paste_method: "ctrl_v",
  typing_tool: "enigo",
  external_script_path: null,
  clipboard_handling: "copy_to_clipboard",
  auto_submit: false,
  auto_submit_key: "enter",
  history_limit: 100,
  recording_retention_period: "never",
  mute_while_recording: false,
  append_trailing_space: true,
  log_level: "info",
  app_language: "en",
  theme: "dark",
  lazy_stream_close: false,
  airpods_mode: false,
  vad_enabled: true,
  vad_backend: "silero",
  long_form_chunking: true,
  filler_word_removal_enabled: true,
  show_tray_icon: true,
  transcribe_accelerator: "auto",
  transcribe_gpu_device: null,
  post_process_enabled: false,
  post_process_selected_prompt: null,
  post_process_provider_id: null,
  post_process_api_key: null,
  post_process_model: null,
  post_process_base_url: null,
  onboarding_completed: true,
  selected_model: "whisper-small",
  bindings: {
    transcribe: {
      id: "transcribe",
      name: "Transcribe",
      description: "Start and stop dictation",
      default_binding: "ctrl",
      current_binding: "ctrl_right",
    },
    cancel: {
      id: "cancel",
      name: "Cancel",
      description: "Cancel the current recording",
      default_binding: "escape",
      current_binding: "escape",
    },
    post_process: {
      id: "post_process",
      name: "Post-process",
      description: "Transcribe and then rewrite",
      default_binding: "",
      current_binding: "",
    },
  },
};

const model = (extra: Record<string, unknown>): Record<string, unknown> => ({
  source: {
    HuggingFace: {
      repo_id: "handy-computer/whisper-medium-gguf",
      revision: "main",
    },
  },
  partial_size: 0,
  accuracy_score: 3,
  speed_score: 4,
  supports_translation: true,
  is_recommended: false,
  supported_languages: ["en", "ru"],
  is_custom: false,
  supports_streaming: false,
  supports_language_detection: true,
  is_downloading: false,
  ...extra,
});

const models = [
  model({
    id: "whisper-small",
    name: "Whisper Small",
    description: "Fast, good for everyday dictation",
    filename: "whisper-medium-Q5_0.gguf",
    source: {
      HuggingFace: {
        repo_id: "handy-computer/whisper-medium-gguf",
        revision: "main",
      },
    },
    size_mb: 466,
    is_downloaded: true,
    supports_language_selection: true,
    is_recommended: true,
  }),
  model({
    id: "whisper-medium",
    name: "Whisper Medium",
    description: "More accurate, slower on CPU",
    filename: "ggml-medium.bin",
    size_mb: 1500,
    is_downloaded: false,
    supports_language_selection: true,
    accuracy_score: 4,
    speed_score: 2,
  }),
  model({
    id: "parakeet",
    name: "Parakeet",
    description: "English, very fast",
    filename: "parakeet-tdt-0.6b-v3-Q5_0.gguf",
    source: {
      HuggingFace: {
        repo_id: "handy-computer/parakeet-tdt-0.6b-v3-gguf",
        revision: "main",
      },
    },
    size_mb: 600,
    is_downloaded: true,
    supports_language_selection: false,
    supported_languages: ["en"],
    supports_language_detection: false,
    speed_score: 5,
  }),
];

const history = {
  entries: [
    {
      id: 3,
      file_name: "3.wav",
      timestamp: 1764000000,
      saved: true,
      title: "Design review",
      transcription_text:
        "The sidebar stays one step darker than the page, and the selected item is a quiet gray fill.",
      post_processed_text: null,
      post_process_prompt: null,
      post_process_requested: false,
      source_name: null,
      language: "en",
    },
    {
      id: 2,
      file_name: "2.wav",
      timestamp: 1763900000,
      saved: false,
      title: "Standup",
      transcription_text:
        "Paste waits until the modifier key is actually up, then sends Ctrl+V.",
      post_processed_text: null,
      post_process_prompt: null,
      post_process_requested: false,
      source_name: null,
      language: "en",
    },
  ],
  has_more: false,
};

export class Channel<T = unknown> {
  onmessage: ((message: T) => void) | null = null;
  constructor() {}
}

export function isTauri() {
  return true;
}

export function convertFileSrc(path: string) {
  return path;
}

export async function invoke<T>(cmd: string, _args?: unknown): Promise<T> {
  switch (cmd) {
    case "get_app_settings":
    case "get_default_settings":
      return structuredClone(settings) as T;
    case "get_available_models":
    case "rescan_local_models":
      return structuredClone(models) as T;
    case "get_current_model":
      return "whisper-small" as T;
    case "get_available_microphones":
    case "get_available_output_devices":
      return [
        { name: "Default", id: "default" },
        { name: "MacBook Microphone", id: "mic-1" },
      ] as T;
    case "is_update_checks_locked":
      return true as T;
    case "get_app_dir_path":
      return "C:\\Users\\Sergei\\AppData\\Roaming\\com.pais.handy" as T;
    case "get_active_notices":
    case "get_retired_models":
    case "get_transcription_jobs":
      return [] as T;
    case "get_history_entries":
      return structuredClone(history) as T;
    case "get_secure_input_status":
      return {
        enabled: false,
        sustained: false,
        culprit_pid: null,
        culprit_name: null,
        fallback_active: false,
      } as T;
    case "get_windows_microphone_permission_status":
      return {
        supported: true,
        overall_access: "granted",
        device_access: "granted",
        app_access: "granted",
        desktop_app_access: "granted",
      } as T;
    case "has_custom_sounds":
      return { start: true, stop: true } as T;
    case "get_post_process_prompts":
    case "list_post_process_prompts":
      return [] as T;
    case "get_transcription_model_status":
      return "ready" as T;
    default:
      console.info(`[preview] ${cmd}`);
      return null as T;
  }
}
