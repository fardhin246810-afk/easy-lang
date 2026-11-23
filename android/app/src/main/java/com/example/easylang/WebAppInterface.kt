package com.example.easylang

import android.content.Context
import android.webkit.JavascriptInterface
import android.webkit.WebView
import java.util.concurrent.Executors

class WebAppInterface(
    private val context: Context,
    private val webView: WebView
) {
    private val executor = Executors.newSingleThreadExecutor()
    private val translator = Translator(context)

    @JavascriptInterface
    fun translate(text: String, srcLang: String, tgtLang: String, callback: String) {
        executor.execute {
            try {
                val result = translator.translate(text, srcLang, tgtLang)
                webView.post {
                    val js = "$callback(${org.json.JSONObject.quote(result)})"
                    webView.evaluateJavascript(js, null)
                }
            } catch (e: Exception) {
                webView.post {
                    val js = "$callback(${org.json.JSONObject.quote("⚠️ ${e.message}")})"
                    webView.evaluateJavascript(js, null)
                }
            }
        }
    }
}
