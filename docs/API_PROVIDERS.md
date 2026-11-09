# Optional text API providers: selective usage

## Supported current integration

`story2kdp.providers.text_task()` and the Streamlit **AI Assistant** tab support opt-in **text responses** via OpenAI, Anthropic Claude and Google Gemini. The adapter uses raw HTTPS via `requests`; API keys are read from `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, and `GEMINI_API_KEY`. You can override model IDs in the UI (models and pricing change).

Anthropic's Claude API is not assumed to generate images. **Image-generation APIs are not implemented in v0.1**. The UI supports importing their images as separate files.

## Selective task workflow

1. Prepare/edit the manuscript and pages locally.
2. Open **AI Assistant** and select exactly one provider/task, e.g., Character Bible, storyboard review or age suitability.
3. Check the full request text. Exclude confidential or copyrighted third-party material you are not authorized to send.
4. Select a supported model ID and explicitly approve sending a paid request.
5. Review output, then manually incorporate accepted advice into the project. **Do not trust arbitrary returned text as production metadata**.
6. Repeat only for specific scenes or tasks that benefit from AI. Identical provider/model/prompt requests are cached locally.

## Costs and limitations

**The MVP does not enforce a hard dollar budget**, nor does it verify provider pricing ahead of execution. Avoid treating the UI approval checkbox as a cost cap. Request no more than the selected output tokens and monitor usage in your provider's dashboard. Failed calls are not automatically retried, but may still be billed by the provider. The cache stores complete prompts/responses and should be secured.

Supported default model IDs are illustrative and may be retired: override them based on current provider documentation. Do not use a personal ChatGPT subscription as a substitute for an OpenAI API key; billing is separate. For actual image APIs and robust usage accounting, implement a separately tested provider adapter with cost reservation and accounting before production.
