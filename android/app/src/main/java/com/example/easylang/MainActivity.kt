package com.example.easylang

import android.annotation.SuppressLint
import android.app.AlertDialog
import android.os.Bundle
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.EditText
import android.widget.LinearLayout
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    private lateinit var webView: WebView
    private val preferences by lazy { getSharedPreferences("easy_lang", MODE_PRIVATE) }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        webView = WebView(this)
        webView.settings.javaScriptEnabled = true
        webView.settings.domStorageEnabled = true
        webView.settings.allowFileAccess = false
        webView.webChromeClient = WebChromeClient()
        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                val url = request?.url ?: return false
                return url.scheme != "http" && url.scheme != "https"
            }
        }
        setContentView(webView)

        val savedServer = preferences.getString("server_url", null)
        if (savedServer.isNullOrBlank()) showServerDialog()
        else openServer(savedServer)
    }

    private fun showServerDialog() {
        val container = LinearLayout(this).apply {
            orientation = LinearLayout.VERTICAL
            setPadding(48, 24, 48, 8)
        }
        container.addView(TextView(this).apply {
            text = "Easy Lang runs translation on your computer. Start api_server.py on the computer, then enter the local address it prints (for example http://192.168.1.20:8000). Keep both devices on the same Wi-Fi."
        })
        val input = EditText(this).apply {
            hint = "http://192.168.1.20:8000"
            setSingleLine(true)
            setText(preferences.getString("server_url", ""))
        }
        container.addView(input)
        AlertDialog.Builder(this)
            .setTitle("Connect to your Easy Lang server")
            .setView(container)
            .setCancelable(false)
            .setPositiveButton("Connect") { _, _ ->
                var address = input.text.toString().trim().trimEnd('/')
                if (!address.startsWith("http://") && !address.startsWith("https://")) address = "http://$address"
                if (address.contains(" ") || address == "http://") {
                    Toast.makeText(this, "Enter a valid local server address.", Toast.LENGTH_LONG).show()
                    showServerDialog()
                } else {
                    preferences.edit().putString("server_url", address).apply()
                    openServer(address)
                }
            }
            .setNeutralButton("How to connect", null)
            .show()
    }

    private fun openServer(address: String) {
        webView.loadUrl(address)
    }

    override fun onBackPressed() {
        if (::webView.isInitialized && webView.canGoBack()) webView.goBack()
        else super.onBackPressed()
    }
}
