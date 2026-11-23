import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Header (Pages > 1)
        if self._pageNumber > 1:
            self.drawString(40, 755, "EASY LANG — Offline Neural Machine Translator")
            self.drawRightString(572, 755, "Mentor Technical Brief")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.75)
            self.line(40, 747, 572, 747)

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.75)
        self.line(40, 42, 572, 42)
        
        self.setFont("Helvetica", 8)
        self.drawString(40, 30, "Confidential — Prepared for Academic & Technical Mentorship Review")
        self.drawRightString(572, 30, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def create_documentation_pdf(filename="Easy_Lang_Project_Documentation.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    primary_color = colors.HexColor("#0f172a") # Slate Navy
    accent_red = colors.HexColor("#ff4b4b")   # Streamlit coral
    accent_blue = colors.HexColor("#2563eb")  # Tech Blue
    text_dark = colors.HexColor("#1e293b")
    text_muted = colors.HexColor("#64748b")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=accent_red,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=accent_blue,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=text_dark,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_dark,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    code_pill_style = ParagraphStyle(
        'CodePill',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#094c9e")
    )

    card_text_style = ParagraphStyle(
        'CardText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=text_dark
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=text_dark
    )

    story = []

    # ==================== COVER / HEADER ====================
    story.append(Paragraph("Easy Lang — Technical Project Documentation", title_style))
    story.append(Paragraph("Offline Neural Machine Translation System · 200+ Languages · Zero-Cloud Architecture", subtitle_style))
    
    # Metadata callout banner
    meta_data = [
        [
            Paragraph("<b>Author / Developer:</b> fardhin246810-afk", card_text_style),
            Paragraph("<b>Repository:</b> github.com/fardhin246810-afk/easy-lang", card_text_style)
        ],
        [
            Paragraph("<b>Model Architecture:</b> Meta NLLB-200 (600M Distilled) + LoRA", card_text_style),
            Paragraph("<b>Inference Mode:</b> 100% On-Device / Air-Gapped (CPU/GPU)", card_text_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[260, 272])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('BORDER', (0,0), (-1,-1), 1, colors.HexColor("#e2e8f0")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # ==================== 1. EXECUTIVE SUMMARY ====================
    story.append(Paragraph("1. Executive Summary & Mentor Overview", h1_style))
    story.append(Paragraph(
        "<b>What is Easy Lang?</b> Most modern translation platforms (Google Translate, DeepL, Microsoft Translator) rely strictly on proprietary cloud APIs that require high-speed internet and process user text on external servers. "
        "<b>Easy Lang</b> solves this through a self-hosted, air-gapped neural machine translation pipeline designed for local execution without telemetry or cloud dependency.",
        body_style
    ))

    # High-level feature cards
    features_data = [
        [
            Paragraph("<b>🔒 Complete Privacy & Air-Gap</b><br/>Zero cloud API calls. All model weights, tokenizer vocabularies, and inference calculations execute entirely on the user's host machine.", card_text_style),
            Paragraph("<b>🌍 200+ Multilingual Reach</b><br/>Powered by Meta's NLLB-200 (No Language Left Behind), accommodating complex non-Latin scripts (Devanagari, Bengali, Cyrillic, Arabic, etc.).", card_text_style),
            Paragraph("<b>⚡ Low-Resource Adaptation</b><br/>Features a parameter-efficient fine-tuning (LoRA) pipeline with tagged stochastic back-translation for underserved language pairs.", card_text_style)
        ]
    ]
    features_table = Table(features_data, colWidths=[174, 174, 174])
    features_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#eff6ff")), # Blue tint
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#f0fdf4")), # Green tint
        ('BACKGROUND', (2,0), (2,0), colors.HexColor("#fff1f2")), # Red tint
        ('BORDER', (0,0), (-1,-1), 0.75, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(features_table)
    story.append(Spacer(1, 10))

    # ==================== 2. COMPLETE TECH STACK ====================
    story.append(Paragraph("2. Comprehensive Tech Stack & Architectural Justification", h1_style))
    story.append(Paragraph(
        "Every library and framework in Easy Lang was selected specifically for high throughput, local hardware efficiency, and zero runtime internet dependencies:",
        body_style
    ))

    tech_data = [
        [
            Paragraph("Layer / Domain", table_header_style),
            Paragraph("Technology & Version", table_header_style),
            Paragraph("Role & Why It Was Chosen", table_header_style)
        ],
        [
            Paragraph("<b>Deep Learning Framework</b>", table_cell_style),
            Paragraph("<b>PyTorch</b> (v2.15)", code_pill_style),
            Paragraph("Provides native tensor execution, automatic mixed precision, CUDA GPU hardware acceleration, and dynamic memory management.", table_cell_style)
        ],
        [
            Paragraph("<b>Neural Model Backbone</b>", table_cell_style),
            Paragraph("<b>Meta NLLB-200</b><br/>(600M Distilled)", code_pill_style),
            Paragraph("State-of-the-art multilingual Seq2Seq architecture supporting 204 languages; 600M distilled checkpoint balances high translation accuracy with practical consumer RAM/VRAM footprints.", table_cell_style)
        ],
        [
            Paragraph("<b>Transformer Orchestration</b>", table_cell_style),
            Paragraph("<b>Hugging Face</b><br/>Transformers (v4.57)", code_pill_style),
            Paragraph("Standardized interface for <code>AutoModelForSeq2SeqLM</code>, handling beam search decoding, forced BOS language tokens, and KV caching.", table_cell_style)
        ],
        [
            Paragraph("<b>Subword Tokenization</b>", table_cell_style),
            Paragraph("<b>SentencePiece</b><br/>(Byte-Level BPE)", code_pill_style),
            Paragraph("Deconstructs words into data-driven subwords (<code>_Clean</code>, <code>_water</code>), resolving Out-of-Vocabulary (OOV) tokens across 200+ distinct scripts.", table_cell_style)
        ],
        [
            Paragraph("<b>Parameter-Efficient Training</b>", table_cell_style),
            Paragraph("<b>PEFT & LoRA</b><br/>(Low-Rank Adaptation)", code_pill_style),
            Paragraph("Freezes 99%+ of base weights and only updates rank decomposition matrices in attention projections (<code>q_proj</code>, <code>v_proj</code>), cutting fine-tuning memory by over 70%.", table_cell_style)
        ],
        [
            Paragraph("<b>Offline Language ID</b>", table_cell_style),
            Paragraph("<b>langid.py</b> & pycountry", code_pill_style),
            Paragraph("High-speed n-gram naive Bayes classifier that detects source languages offline in under 2ms without making any external cloud network requests.", table_cell_style)
        ],
        [
            Paragraph("<b>Web Application Framework</b>", table_cell_style),
            Paragraph("<b>Streamlit</b> (v1.67)", code_pill_style),
            Paragraph("Native Python web framework providing reactive UI, session state, sliders, and automatic local-network LAN sharing for mobile device access.", table_cell_style)
        ],
        [
            Paragraph("<b>Standalone Web Frontend</b>", table_cell_style),
            Paragraph("<b>HTML5 / CSS3 / Vanilla JS</b>", code_pill_style),
            Paragraph("Self-contained, zero-dependency client interface matching Streamlit's dark/light design with client-side token visualizer and Web Speech API audio.", table_cell_style)
        ],
        [
            Paragraph("<b>Evaluation & Quality</b>", table_cell_style),
            Paragraph("<b>SacreBLEU</b> (v2.6)", code_pill_style),
            Paragraph("Industry standard reproducibility metric computing corpus BLEU and character n-gram F-score (chrF++) to evaluate translation quality on validation sets.", table_cell_style)
        ]
    ]

    tech_table = Table(tech_data, colWidths=[120, 115, 297])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(tech_table)

    story.append(PageBreak()) # Clean page break for Workflow & Pipeline

    # ==================== 3. SYSTEM WORKFLOW ====================
    story.append(Paragraph("3. End-to-End System Workflow (How Translation Works)", h1_style))
    story.append(Paragraph(
        "To explain the architecture clearly to a mentor, the translation pipeline can be visualized as four distinct operational phases:",
        body_style
    ))

    workflow_data = [
        [
            Paragraph("Phase 1<br/><b>Input & Offline Detection</b>", table_header_style),
            Paragraph("Phase 2<br/><b>SentencePiece Tokenization</b>", table_header_style),
            Paragraph("Phase 3<br/><b>Seq2Seq Neural Inference</b>", table_header_style),
            Paragraph("Phase 4<br/><b>Detokenization & Delivery</b>", table_header_style)
        ],
        [
            Paragraph(
                "• User types text or selects a sample.<br/>"
                "• <b>Offline Identifier</b> (<code>langid</code>) extracts character n-gram frequencies.<br/>"
                "• Maps language to NLLB ISO code (e.g., English -> <code>eng_Latn</code>, Hindi -> <code>hin_Deva</code>).<br/>"
                "• User can override with manual dropdown.",
                table_cell_style
            ),
            Paragraph(
                "• Sets <code>tokenizer.src_lang</code>.<br/>"
                "• Segmenter decomposes words into subword units (e.g. <code>_Clean</code>, <code>_water</code>).<br/>"
                "• Converts characters to numerical token IDs.<br/>"
                "• Generates PyTorch input tensors + attention masks (max len: 256).",
                table_cell_style
            ),
            Paragraph(
                "• Target language set via <code>forced_bos_token_id</code>.<br/>"
                "• <b>Encoder</b> creates contextual embeddings.<br/>"
                "• <b>Autoregressive Decoder</b> evaluates word likelihoods.<br/>"
                "• <b>Beam Search</b> (width 1-6) tracks top probability candidate branches simultaneously.",
                table_cell_style
            ),
            Paragraph(
                "• Translates output IDs back into human characters.<br/>"
                "• Strips special symbols (<code>&lt;s&gt;</code>, <code>&lt;/s&gt;</code>, language tags).<br/>"
                "• Displays final translation in UI.<br/>"
                "• Renders visual subword token chips for model inspectability.",
                table_cell_style
            )
        ]
    ]

    workflow_table = Table(workflow_data, colWidths=[133, 133, 133, 133])
    workflow_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1e293b")),
        ('GRID', (0,0), (-1,-1), 0.75, colors.HexColor("#94a3b8")),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor("#f8fafc")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(workflow_table)
    story.append(Spacer(1, 10))

    # Beam search explanation box
    story.append(Paragraph("<b>Understanding the Beam Search Slider (Mentor Highlight):</b>", h2_style))
    story.append(Paragraph(
        "In simple greedy decoding (Beam = 1), the neural network picks only the single highest-probability next word at each step, which often leads to repetitive or unnatural grammar. "
        "With <b>Beam Search (Width = 4)</b>, the model maintains the 4 most promising overall sentence paths simultaneously, pruning low-scoring combinations until completion. "
        "This drastically elevates grammatical fluency with only modest computational overhead.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # ==================== 4. AUTOMATION & TRAINING PIPELINE ====================
    story.append(Paragraph("4. Automation & Fine-Tuning Pipeline", h1_style))
    story.append(Paragraph(
        "Easy Lang is not just a static translation UI; it includes an automated end-to-end training and data pipeline for expanding to rare, low-resource dialects:",
        body_style
    ))

    auto_data = [
        [
            Paragraph("Automated Pipeline Stage", table_header_style),
            Paragraph("Implementation in Code (Script & Logic)", table_header_style),
            Paragraph("Technical Purpose & Significance", table_header_style)
        ],
        [
            Paragraph("<b>Automated Model Ingestion</b>", table_cell_style),
            Paragraph("<code>download_model.py</code>", code_pill_style),
            Paragraph("Automatically pulls weights and configurations once from Hugging Face Hub, verifies hash integrity, and stores them in <code>models/</code> for perpetual offline operation.", table_cell_style)
        ],
        [
            Paragraph("<b>Corpus Sanitization & Dedup</b>", table_cell_style),
            Paragraph("<code>train_mt.py</code>: <code>clean_pairs()</code>", code_pill_style),
            Paragraph("Strips corrupt rows, blanks, and exact duplicates from parallel training data, ensuring the neural network doesn't overfit to noise.", table_cell_style)
        ],
        [
            Paragraph("<b>Tagged Stochastic Back-Translation</b>", table_cell_style),
            Paragraph("<code>train_mt.py</code>: <code>synthesize_backtranslation()</code>", code_pill_style),
            Paragraph("Takes unaligned target-language sentences (<code>mono_target.txt</code>) and automatically reverse-translates them to source text. Adds a <code>&lt;BT&gt;</code> prefix tag so the model learns grammar without learning false alignment.", table_cell_style)
        ],
        [
            Paragraph("<b>Memory-Optimized Training</b>", table_cell_style),
            Paragraph("Dynamic Padding & Gradient Accumulation", code_pill_style),
            Paragraph("Pads batches dynamically to the longest sentence in that specific batch rather than global max length. Uses 4-step gradient accumulation to emulate large batch sizes on modest consumer GPUs.", table_cell_style)
        ],
        [
            Paragraph("<b>Automated Evaluation & Checkpointing</b>", table_cell_style),
            Paragraph("Validation chrF / BLEU Tracking", code_pill_style),
            Paragraph("After every training epoch, automatically calculates validation chrF scores. Only saves checkpoints that outperform previous iterations, preventing model regression.", table_cell_style)
        ]
    ]

    auto_table = Table(auto_data, colWidths=[130, 140, 262])
    auto_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(auto_table)

    story.append(PageBreak()) # Clean page break for Languages & Mentor Q&A

    # ==================== 5. USAGE OF CODE LANGUAGES ====================
    story.append(Paragraph("5. Usage of Code Languages: Where & For What Purpose", h1_style))
    story.append(Paragraph(
        "A clear breakdown of why each programming and markup language was used across the project repository:",
        body_style
    ))

    lang_data = [
        [
            Paragraph("Language", table_header_style),
            Paragraph("Files Used In", table_header_style),
            Paragraph("Primary Role & Purpose", table_header_style),
            Paragraph("Key Responsibilities", table_header_style)
        ],
        [
            Paragraph("<b>Python</b><br/><code>.py</code>", table_cell_style),
            Paragraph("<code>app.py</code><br/><code>train_mt.py</code><br/><code>download_model.py</code><br/><code>language_support.py</code><br/><code>mt_config.py</code>", code_pill_style),
            Paragraph("<b>Core Backend & ML Engine</b>", table_cell_style),
            Paragraph("• Loads PyTorch tensors & NLLB weights into memory.<br/>• Orchestrates LoRA parameter adaptation.<br/>• Manages SentencePiece tokenization & beam search.<br/>• Computes SacreBLEU metrics & runs unit tests.", table_cell_style)
        ],
        [
            Paragraph("<b>HTML5</b><br/><code>.html</code>", table_cell_style),
            Paragraph("<code>index.html</code>", code_pill_style),
            Paragraph("<b>Semantic Interface Structure</b>", table_cell_style),
            Paragraph("• Defines form controls, textareas, and radio buttons.<br/>• Structures the Streamlit-inspired layout.<br/>• Houses accessibility tags and SVG vector icons.", table_cell_style)
        ],
        [
            Paragraph("<b>CSS3</b><br/><code>&lt;style&gt;</code>", table_cell_style),
            Paragraph("Embedded in<br/><code>index.html</code>", code_pill_style),
            Paragraph("<b>Responsive Visual Styling</b>", table_cell_style),
            Paragraph("• Replicates exact Streamlit dark theme (<code>#0e1117</code>).<br/>• Provides dynamic Dark / Light mode theming.<br/>• Styles animated sidebar, toggle switches & spinners.<br/>• Adapts layout seamlessly for laptops and smartphones.", table_cell_style)
        ],
        [
            Paragraph("<b>JavaScript</b><br/><code>(Vanilla ES6)</code>", table_cell_style),
            Paragraph("Embedded in<br/><code>index.html</code>", code_pill_style),
            Paragraph("<b>Client Reactivity & Offline Simulation</b>", table_cell_style),
            Paragraph("• Real-time regex script detection (Devanagari, Cyrillic, Arabic).<br/>• Simulates SentencePiece subword tokenization visualizer.<br/>• Integrates browser <code>speechSynthesis</code> for audio playback.<br/>• Manages clipboard copy/paste and keyboard shortcuts (R, C).", table_cell_style)
        ],
        [
            Paragraph("<b>PowerShell / Bash</b><br/><code>.ps1</code> / CLI", table_cell_style),
            Paragraph("Terminal Commands & Virtual Environment", code_pill_style),
            Paragraph("<b>Environment & Version Control</b>", table_cell_style),
            Paragraph("• Installs dependencies and activates virtual environments.<br/>• Automates Git repository setup and GitHub sync.<br/>• Launches Streamlit servers with LAN binding (<code>0.0.0.0</code>).", table_cell_style)
        ]
    ]

    lang_table = Table(lang_data, colWidths=[65, 115, 145, 207])
    lang_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('PADDING', (0,0), (-1,-1), 4.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(lang_table)
    story.append(Spacer(1, 10))

    # ==================== 6. MENTOR Q&A PITCH ====================
    story.append(Paragraph("6. Quick-Fire Mentor Q&A (How to Present Confidently)", h1_style))

    qa_items = [
        ("Q: Why not just call Google Translate API or OpenAI API?",
         "<b>A:</b> Commercial APIs have three critical flaws: they mandate constant internet access, charge ongoing per-character API fees, and transmit private enterprise/patient/personal text to third-party servers. Easy Lang runs 100% locally with zero subscription costs and absolute privacy."),
        
        ("Q: How does this run on a normal computer without 40GB VRAM?",
         "<b>A:</b> We utilize the <b>Distilled 600M</b> variant of NLLB-200. Meta trained this through knowledge distillation from their massive 54-billion parameter teacher model. It delivers enterprise-grade BLEU scores in a lightweight 2.4GB footprint that executes comfortably on consumer CPUs and 6GB-8GB GPUs."),

        ("Q: Why LoRA instead of standard full model fine-tuning?",
         "<b>A:</b> Full fine-tuning updates all 600 million parameters and requires storing multi-gigabyte optimizer states. LoRA freezes the base weights and injects small rank-16 low-rank matrices into attention layers, updating less than 1% of the model. This makes training 3x faster and allows instant model swapping."),

        ("Q: What is the purpose of having both app.py and index.html?",
         "<b>A:</b> <code>app.py</code> is the full Python Streamlit server that connects directly to the local PyTorch model weights for actual on-device neural inference. <code>index.html</code> is a standalone, ultra-fast web interface that can be previewed or hosted anywhere with instant client-side token inspection, speech synthesis, and mock fallbacks without needing Python running.")
    ]

    for q, a in qa_items:
        story.append(Paragraph(q, h2_style))
        story.append(Paragraph(a, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    return filename

if __name__ == "__main__":
    out_file = "Easy_Lang_Project_Documentation.pdf"
    if len(sys.argv) > 1:
        out_file = sys.argv[1]
    create_documentation_pdf(out_file)
    print(f"Successfully generated: {os.path.abspath(out_file)}")
