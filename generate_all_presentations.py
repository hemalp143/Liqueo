#!/usr/bin/env python3
"""Generate all presentation and documentation files for Liqueo project."""

import subprocess
import sys

print("\n" + "="*70)
print("🎨 GENERATING ALL LIQUEO PRESENTATIONS & DOCUMENTATION")
print("="*70 + "\n")

scripts = [
    ("Demo Package PDF", "generate_pdf.py"),
    ("Demo Presentation PPTX", "generate_pptx.py"),
    ("Supervisor Presentation", "create_supervisor_pptx.py"),
    ("Final Report PDF", "create_final_report.py"),
    ("Professional Documentation", "create_professional_report.py"),
]

failed = []
generated = []

for name, script in scripts:
    print(f"⏳ Generating {name}... ({script})")
    try:
        result = subprocess.run([sys.executable, script], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"   ✅ {name} created successfully\n")
            generated.append(name)
        else:
            print(f"   ❌ Error: {result.stderr}\n")
            failed.append((name, result.stderr))
    except subprocess.TimeoutExpired:
        print(f"   ❌ Timeout\n")
        failed.append((name, "Timeout"))
    except Exception as e:
        print(f"   ❌ Error: {e}\n")
        failed.append((name, str(e)))

print("="*70)
print(f"✅ SUCCESSFULLY GENERATED: {len(generated)}")
print("="*70)
for item in generated:
    print(f"  ✓ {item}")

if failed:
    print("\n" + "="*70)
    print(f"❌ FAILED: {len(failed)}")
    print("="*70)
    for name, error in failed:
        print(f"  ✗ {name}: {error[:60]}")
else:
    print("\n🎉 All presentations and documentation generated successfully!")

print("\n" + "="*70)
print("📄 DELIVERABLES SUMMARY")
print("="*70 + "\n")

import os
import glob

pdfs = glob.glob("Liqueo_*.pdf")
pptxs = glob.glob("Liqueo_*.pptx")

print("📋 PDF Files:")
for pdf in sorted(pdfs):
    size = os.path.getsize(pdf) / 1024
    print(f"  • {pdf} ({size:.1f} KB)")

print("\n📊 PowerPoint Files:")
for pptx in sorted(pptxs):
    size = os.path.getsize(pptx) / 1024
    print(f"  • {pptx} ({size:.1f} KB)")

print("\n" + "="*70 + "\n")
