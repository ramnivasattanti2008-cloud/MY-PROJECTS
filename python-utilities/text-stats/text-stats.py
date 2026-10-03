#!/usr/bin/env python3
"""
Text Statistics Analyzer - Analyze text files for statistics and readability.
"""

import os
import sys
import argparse
import re
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox, scrolledtext
    HAS_TK = True
except ImportError:
    HAS_TK = False


class TextAnalyzer:
    """Analyze text files for statistics and readability metrics."""

    def __init__(self):
        self.text = ""
        self.words = []
        self.sentences = []
        self.paragraphs = []

        # Statistics
        self.stats = {
            'characters': 0,
            'characters_no_spaces': 0,
            'words': 0,
            'unique_words': 0,
            'sentences': 0,
            'paragraphs': 0,
            'lines': 0,
            'avg_word_length': 0,
            'avg_sentence_length': 0,
            'avg_words_per_paragraph': 0,
            'word_frequency': [],
            'sentence_length_distribution': [],
            'syllable_count': 0,
            'avg_syllables_per_word': 0,
        }

        # Readability scores
        self.readability = {
            'flesch_reading_ease': 0,
            'flesch_kincaid_grade': 0,
            'gunning_fog': 0,
            'smog_index': 0,
            'ari': 0,
            'coleman_liau': 0,
        }

        self.top_words = []

    def load_file(self, filepath: str) -> str:
        """Load text from file."""
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            self.text = f.read()
        return self.text

    def load_text(self, text: str):
        """Load text directly."""
        self.text = text

    def analyze(self):
        """Perform full analysis of loaded text."""
        if not self.text:
            return

        self._tokenize()
        self._calculate_basic_stats()
        self._calculate_readability()

    def _tokenize(self):
        """Tokenize text into words, sentences, paragraphs."""
        # Words
        self.words = re.findall(r"[a-zA-Z']+", self.text.lower())

        # Sentences (split by . ! ?)
        self.sentences = re.split(r'[.!?]+', self.text)
        self.sentences = [s.strip() for s in self.sentences if s.strip()]

        # Paragraphs (split by double newlines)
        self.paragraphs = re.split(r'\n\s*\n', self.text)
        self.paragraphs = [p.strip() for p in self.paragraphs if p.strip()]

        # Lines
        self.lines = [line for line in self.text.split('\n') if line.strip()]

    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word (approximate)."""
        word = word.lower()
        if len(word) <= 3:
            return 1

        # Remove silent e at end
        if word.endswith('e'):
            word = word[:-1]

        # Count vowel groups
        count = len(re.findall(r'[aeiouy]+', word))

        # Adjust for common patterns
        if word.endswith('le') and len(word) > 2 and word[-3] not in 'aeiouy':
            count += 1

        return max(1, count)

    def _calculate_basic_stats(self):
        """Calculate basic text statistics."""
        # Character counts
        self.stats['characters'] = len(self.text)
        self.stats['characters_no_spaces'] = len(self.text.replace(' ', ''))

        # Word counts
        self.stats['words'] = len(self.words)
        self.stats['unique_words'] = len(set(self.words))

        # Sentence counts
        self.stats['sentences'] = len(self.sentences)

        # Paragraph counts
        self.stats['paragraphs'] = len(self.paragraphs)

        # Line counts
        self.stats['lines'] = len(self.lines)

        # Averages
        if self.words:
            self.stats['avg_word_length'] = sum(len(w) for w in self.words) / len(self.words)

        if self.sentences:
            sentence_lengths = [len(s.split()) for s in self.sentences]
            self.stats['avg_sentence_length'] = sum(sentence_lengths) / len(sentence_lengths)
            self.stats['sentence_length_distribution'] = sentence_lengths

        if self.paragraphs and self.words:
            self.stats['avg_words_per_paragraph'] = self.stats['words'] / len(self.paragraphs)

        # Syllables
        if self.words:
            total_syllables = sum(self._count_syllables(w) for w in self.words)
            self.stats['syllable_count'] = total_syllables
            self.stats['avg_syllables_per_word'] = total_syllables / len(self.words)

        # Word frequency
        word_counts = Counter(self.words)
        # Filter stopwords for top words
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                    'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare',
                    'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as',
                    'into', 'through', 'during', 'before', 'after', 'above', 'below',
                    'and', 'but', 'or', 'nor', 'so', 'yet', 'both', 'either', 'neither',
                    'not', 'only', 'own', 'same', 'than', 'too', 'very', 'just', 'also'}

        content_words = [(w, c) for w, c in word_counts.most_common(50) if w not in stopwords]
        self.stats['word_frequency'] = content_words[:20]
        self.top_words = content_words[:10]

    def _calculate_readability(self):
        """Calculate readability indices."""
        words = self.stats['words']
        sentences = max(1, self.stats['sentences'])
        syllables = self.stats['syllable_count']
        chars = sum(len(w) for w in self.words)

        if words == 0:
            return

        # Flesch Reading Ease
        # 206.835 - 1.015(words/sentences) - 84.6(syllables/words)
        self.readability['flesch_reading_ease'] = (
            206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
        )

        # Flesch-Kincaid Grade Level
        # 0.39(words/sentences) + 11.8(syllables/words) - 15.59
        self.readability['flesch_kincaid_grade'] = (
            0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59
        )

        # Gunning Fog Index
        # 0.4((words/sentences) + 100((complex_words/words)))
        complex_words = sum(1 for w in self.words if self._count_syllables(w) >= 3)
        self.readability['gunning_fog'] = (
            0.4 * ((words / sentences) + 100 * (complex_words / words))
        )

        # SMOG Index (simplified)
        # 1.0430 * sqrt(complex_words * (30/sentences)) + 3.1291
        if sentences >= 30:
            self.readability['smog_index'] = (
                1.0430 * (complex_words * (30 / sentences)) ** 0.5 + 3.1291
            )

        # Automated Readability Index (ARI)
        # 4.71(chars/words) + 0.5(words/sentences) - 21.43
        self.readability['ari'] = (
            4.71 * (chars / words) + 0.5 * (words / sentences) - 21.43
        )

        # Coleman-Liau Index
        # 0.0588 * (100*chars/words) - 0.296*(100*sentences/words) - 15.8
        L = (chars / words) * 100  # avg letters per 100 words
        S = (sentences / words) * 100  # avg sentences per 100 words
        self.readability['coleman_liau'] = (0.0588 * L - 0.296 * S - 15.8)

    def get_summary(self) -> str:
        """Get formatted summary of analysis."""
        s = self.stats
        r = self.readability

        lines = [
            "=" * 60,
            "TEXT STATISTICS ANALYSIS",
            "=" * 60,
            "",
            "BASIC STATISTICS",
            "-" * 40,
            f"Characters:          {s['characters']:,}",
            f"  (without spaces):  {s['characters_no_spaces']:,}",
            f"Words:               {s['words']:,}",
            f"  Unique words:     {s['unique_words']:,}",
            f"  Avg word length:   {s['avg_word_length']:.2f}",
            f"Sentences:           {s['sentences']:,}",
            f"  Avg sentence len:  {s['avg_sentence_length']:.1f} words",
            f"Paragraphs:          {s['paragraphs']:,}",
            f"Lines:               {s['lines']:,}",
            "",
            "VOCABULARY ANALYSIS",
            "-" * 40,
            f"Total syllables:    {s['syllable_count']:,}",
            f"Avg syllables/word: {s['avg_syllables_per_word']:.2f}",
            f"Lexical diversity:  {(s['unique_words']/s['words']*100):.1f}%",
            "",
            "READABILITY INDICES",
            "-" * 40,
            f"Flesch Reading Ease:      {r['flesch_reading_ease']:.1f}",
            f"  (higher = easier, 60-70 is ideal)",
            f"Flesch-Kincaid Grade:     {r['flesch_kincaid_grade']:.1f}",
            f"  (US grade level required)",
            f"Gunning Fog Index:         {r['gunning_fog']:.1f}",
            f"  (years of education needed)",
            f"SMOG Index:               {r['smog_index']:.1f}",
            f"Automated Readability:    {r['ari']:.1f}",
            f"Coleman-Liau Index:       {r['coleman_liau']:.1f}",
            "",
        ]

        if self.top_words:
            lines.extend([
                "TOP 10 CONTENT WORDS",
                "-" * 40,
            ])
            for i, (word, count) in enumerate(self.top_words, 1):
                lines.append(f"  {i:2}. {word:<15} ({count} occurrences)")

        lines.extend([
            "",
            "=" * 60,
        ])

        return '\n'.join(lines)

    def get_readability_interpretation(self) -> str:
        """Get interpretation of readability scores."""
        fre = self.readability['flesch_reading_ease']

        if fre >= 90:
            return "Very Easy (5th grade)"
        elif fre >= 80:
            return "Easy (6th grade)"
        elif fre >= 70:
            return "Fairly Easy (7th grade)"
        elif fre >= 60:
            return "Standard (8th-9th grade)"
        elif fre >= 50:
            return "Fairly Difficult (10th-12th grade)"
        elif fre >= 30:
            return "Difficult (College level)"
        else:
            return "Very Difficult (Graduate level)"


class TextStatsGUI:
    """GUI for text statistics analyzer."""

    def __init__(self, root):
        self.root = root
        self.root.title("Text Statistics Analyzer")
        self.root.geometry("800x700")
        self.root.configure(bg='#1e1e2e')

        self.analyzer = TextAnalyzer()
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        """Configure ttk styles."""
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Dark.TFrame', background='#1e1e2e')
        style.configure('Dark.TLabel', background='#1e1e2e', foreground='#cdd6f4', font=('Segoe UI', 9))
        style.configure('Title.TLabel', background='#1e1e2e', foreground='#f5c2e7', font=('Segoe UI', 14, 'bold'))
        style.configure('Section.TLabel', background='#1e1e2e', foreground='#89b4fa',
                      font=('Segoe UI', 10, 'bold'))
        style.configure('Stat.TLabel', background='#1e1e2e', foreground='#a6e3a1',
                      font=('Segoe UI', 9))
        style.configure('Dark.TButton', background='#313244', foreground='#cdd6f4')
        style.map('Dark.TButton', background=[('active', '#45475a')])

    def create_widgets(self):
        """Create GUI widgets."""
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)

        # Title
        ttk.Label(main_frame, text="Text Statistics Analyzer", style='Title.TLabel').pack(pady=(0, 10))

        # Input section
        input_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        input_frame.pack(fill='x', pady=10)

        ttk.Button(input_frame, text="Load File", command=self.load_file).pack(side='left', padx=5)

        self.file_label = ttk.Label(input_frame, text="No file loaded", style='Dark.TLabel')
        self.file_label.pack(side='left', padx=10)

        ttk.Button(input_frame, text="Analyze Sample", command=self.load_sample).pack(side='left', padx=5)
        ttk.Button(input_frame, text="Clear", command=self.clear).pack(side='left', padx=5)

        # Text input
        ttk.Label(main_frame, text="Or enter/paste text:", style='Dark.TLabel').pack(anchor='w', pady=(10, 5))
        self.text_input = scrolledtext.ScrolledText(main_frame, height=8, bg='#313244',
                                                     fg='#cdd6f4', font=('Segoe UI', 9))
        self.text_input.pack(fill='x', pady=5)

        ttk.Button(main_frame, text="Analyze Text", command=self.analyze_text).pack(pady=5)

        # Results notebook
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True, pady=10)

        # Basic stats tab
        self.stats_frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(self.stats_frame, text="Basic Statistics")

        # Readability tab
        self.readability_frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(self.readability_frame, text="Readability")

        # Word frequency tab
        self.words_frame = ttk.Frame(notebook, style='Dark.TFrame')
        notebook.add(self.words_frame, text="Word Frequency")

        # Canvas for scrollable results
        self.create_stats_content()
        self.create_readability_content()
        self.create_words_content()

    def create_stats_content(self):
        """Create basic statistics content area."""
        canvas = tk.Canvas(self.stats_frame, bg='#1e1e2e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.stats_frame, orient='vertical', command=canvas.yview)
        content = ttk.Frame(canvas, style='Dark.TFrame')

        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=content, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        self.stats_labels = {}

        # Create stat rows
        categories = [
            ("Characters", ['characters', 'characters_no_spaces']),
            ("Words", ['words', 'unique_words', 'avg_word_length']),
            ("Sentences", ['sentences', 'avg_sentence_length']),
            ("Paragraphs & Lines", ['paragraphs', 'lines', 'avg_words_per_paragraph']),
            ("Syllables", ['syllable_count', 'avg_syllables_per_word']),
        ]

        row = 0
        for cat, fields in categories:
            ttk.Label(content, text=cat, style='Section.TLabel').grid(row=row, column=0, columnspan=2, sticky='w', pady=(10, 5))
            row += 1

            for field in fields:
                label = tk.Label(content, text=f"{field}: -", bg='#1e1e2e', fg='#a6e3a1',
                               font=('Segoe UI', 9), anchor='w')
                label.grid(row=row, column=0, columnspan=2, sticky='w', padx=20)
                self.stats_labels[field] = label
                row += 1

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def create_readability_content(self):
        """Create readability content area."""
        canvas = tk.Canvas(self.readability_frame, bg='#1e1e2e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.readability_frame, orient='vertical', command=canvas.yview)
        content = ttk.Frame(canvas, style='Dark.TFrame')

        content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=content, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        self.readability_labels = {}

        indices = [
            ("Flesch Reading Ease", "flesch_reading_ease", "0-100 (higher = easier)"),
            ("Flesch-Kincaid Grade", "flesch_kincaid_grade", "US grade level"),
            ("Gunning Fog Index", "gunning_fog", "Years of education needed"),
            ("SMOG Index", "smog_index", "Years of education needed"),
            ("Automated Readability", "ari", "US grade level"),
            ("Coleman-Liau Index", "coleman_liau", "US grade level"),
        ]

        self.interpretation_label = tk.Label(content, text="", bg='#1e1e2e', fg='#f5c2e7',
                                             font=('Segoe UI', 11, 'bold'))
        self.interpretation_label.pack(pady=10)

        for i, (name, key, desc) in enumerate(indices):
            frame = ttk.Frame(content, style='Dark.TFrame')
            frame.pack(fill='x', pady=5, padx=10)

            ttk.Label(frame, text=f"{name}:", style='Dark.TLabel').pack(side='left')
            label = tk.Label(frame, text="-", bg='#181825', fg='#a6e3a1',
                           font=('Consolas', 10), width=10)
            label.pack(side='left', padx=10)
            self.readability_labels[key] = label

            ttk.Label(frame, text=f"({desc})", style='Dark.TLabel').pack(side='left')

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def create_words_content(self):
        """Create word frequency content area."""
        canvas = tk.Canvas(self.words_frame, bg='#1e1e2e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.words_frame, orient='vertical', command=canvas.yview)
        self.words_content = ttk.Frame(canvas, style='Dark.TFrame')

        self.words_content.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.create_window((0, 0), window=self.words_content, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        self.words_label = tk.Label(self.words_content, text="No analysis yet", bg='#1e1e2e',
                                   fg='#6c7086', font=('Segoe UI', 10))
        self.words_label.pack(padx=20, pady=20)

        canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def load_file(self):
        """Load a text file."""
        filepath = filedialog.askopenfilename(
            title="Select Text File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filepath:
            self.analyzer.load_file(filepath)
            self.file_label.config(text=os.path.basename(filepath))
            self.text_input.delete('1.0', 'end')
            self.text_input.insert('1.0', self.analyzer.text[:1000] + "..." if len(self.analyzer.text) > 1000 else self.analyzer.text)
            self.analyze()

    def load_sample(self):
        """Load sample text for demonstration."""
        sample = """
        The quick brown fox jumps over the lazy dog. This pangram contains every letter
        of the alphabet at least once. Pangrams are often used to display typefaces and
        test keyboards.

        Text analysis is an important field in natural language processing. It involves
        examining text to extract meaningful information. This can include counting words,
        analyzing sentence structure, and measuring readability.

        Readability scores help determine how easy a text is to understand. The Flesch
        Reading Ease score uses sentence length and syllable count to estimate reading level.
        A score of 60-70 is considered ideal for most documents.

        Natural language processing continues to evolve rapidly. Machine learning models
        can now understand context and nuance in ways that were impossible just a decade ago.
        """
        self.text_input.delete('1.0', 'end')
        self.text_input.insert('1.0', sample)
        self.file_label.config(text="Sample text")
        self.analyze_text()

    def clear(self):
        """Clear all results."""
        self.text_input.delete('1.0', 'end')
        self.file_label.config(text="No file loaded")
        self.analyzer = TextAnalyzer()
        self.update_display()

    def analyze_text(self):
        """Analyze text from input field."""
        text = self.text_input.get('1.0', 'end').strip()
        if not text:
            messagebox.showwarning("No Text", "Please enter some text to analyze.")
            return

        self.analyzer.load_text(text)
        self.analyze()

    def analyze(self):
        """Run analysis and update display."""
        self.analyzer.analyze()
        self.update_display()

    def update_display(self):
        """Update all display elements."""
        s = self.analyzer.stats
        r = self.analyzer.readability

        # Update stats
        self.stats_labels.get('characters', tk.Label()).config(text=f"Total: {s['characters']:,}")
        self.stats_labels.get('characters_no_spaces', tk.Label()).config(text=f"Without spaces: {s['characters_no_spaces']:,}")
        self.stats_labels.get('words', tk.Label()).config(text=f"Total: {s['words']:,}")
        self.stats_labels.get('unique_words', tk.Label()).config(text=f"Unique: {s['unique_words']:,}")
        self.stats_labels.get('avg_word_length', tk.Label()).config(text=f"Average: {s['avg_word_length']:.2f} chars")
        self.stats_labels.get('sentences', tk.Label()).config(text=f"Total: {s['sentences']:,}")
        self.stats_labels.get('avg_sentence_length', tk.Label()).config(text=f"Average: {s['avg_sentence_length']:.1f} words")
        self.stats_labels.get('paragraphs', tk.Label()).config(text=f"Total: {s['paragraphs']:,}")
        self.stats_labels.get('lines', tk.Label()).config(text=f"Total: {s['lines']:,}")
        self.stats_labels.get('avg_words_per_paragraph', tk.Label()).config(text=f"Average: {s['avg_words_per_paragraph']:.1f} words")
        self.stats_labels.get('syllable_count', tk.Label()).config(text=f"Total: {s['syllable_count']:,}")
        self.stats_labels.get('avg_syllables_per_word', tk.Label()).config(text=f"Average: {s['avg_syllables_per_word']:.2f}")

        # Update readability
        for key, label in self.readability_labels.items():
            value = r.get(key, 0)
            label.config(text=f"{value:.1f}")

        self.interpretation_label.config(text=self.analyzer.get_readability_interpretation())

        # Update word frequency
        if self.analyzer.top_words:
            words_text = "Top Content Words (stopwords excluded):\n\n"
            for i, (word, count) in enumerate(self.analyzer.top_words, 1):
                bar = "█" * min(count, 30)
                words_text += f"{i:2}. {word:<15} {bar} ({count})\n"
            self.words_label.config(text=words_text, fg='#a6e3a1', font=('Consolas', 9))
        else:
            self.words_label.config(text="No analysis yet", fg='#6c7086')


def main():
    parser = argparse.ArgumentParser(description="Text Statistics Analyzer")
    parser.add_argument('file', nargs='?', help="Text file to analyze")
    parser.add_argument('-o', '--output', help="Save results to file")
    parser.add_argument('--gui', action='store_true', help="Force GUI mode")
    parser.add_argument('--no-gui', action='store_true', help="Force CLI mode")
    parser.add_argument('--text', help="Analyze specific text")

    args = parser.parse_args()

    use_gui = (args.gui or (not args.no_gui and not args.file and not args.text and HAS_TK and sys.stdout.isatty()))

    if use_gui and HAS_TK:
        root = tk.Tk()
        TextStatsGUI(root)
        root.mainloop()
    else:
        analyzer = TextAnalyzer()

        if args.text:
            analyzer.load_text(args.text)
        elif args.file:
            if not os.path.exists(args.file):
                print(f"Error: File not found: {args.file}")
                return 1
            analyzer.load_file(args.file)
        else:
            print("Text Statistics Analyzer")
            print("Usage: text-stats.py <file> [options]")
            print("       text-stats.py --gui  (to launch GUI)")
            print("\nOptions:")
            print("  --text 'TEXT'    Analyze specific text")
            print("  -o, --output     Save results to file")
            return 1

        analyzer.analyze()
        output = analyzer.get_summary()

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Results saved to {args.output}")
        else:
            print(output)

        return 0


if __name__ == '__main__':
    sys.exit(main())
