import sys
import json
import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

# Parse args
slug = "history-ai-math-to-model"
episode = "ep1"

for i, arg in enumerate(sys.argv):
    if arg == "--slug" and i + 1 < len(sys.argv):
        slug = sys.argv[i+1].lower()
    elif arg == "--episode" and i + 1 < len(sys.argv):
        episode = sys.argv[i+1].lower()

print(f"🎬 Compiling video for project: {slug} | Episode: {episode}")

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSERT_PLAN_PATH = os.path.join(BASE_DIR, f"src/{slug}/edit/{episode}-insert-plan.json")
VOICEOVER_PATH = os.path.join(BASE_DIR, f"public/{slug}/voiceover/{episode}.mp3")
GENERATED_DIR = os.path.join(BASE_DIR, f"public/{slug}/generated")
OUT_DIR = os.path.join(BASE_DIR, f"out/{slug}")
SCRATCH_DIR = os.path.join(BASE_DIR, "scratch")

# Create output and scratch dirs
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(SCRATCH_DIR, exist_ok=True)

# Select font
FONT_PATH = "/System/Library/Fonts/Supplemental/Ayuthaya.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
print(f"Using font: {FONT_PATH}")

# Slide dimensions
WIDTH, HEIGHT = 1080, 1920

def create_text_slide(text_lines, filename, slug_val, title_size=75, body_size=50):
    # Select theme based on project slug
    if "computer" in slug_val:
        bg_color = "#0c0a12" # Dark purple for computer history
        border_color = "#2e1a47"
        inner_border = "#150b24"
        accent_color = "#d946ef" # Neon Magenta
    else:
        bg_color = "#080c14" # Cyber dark blue for AI history
        border_color = "#1e293b"
        inner_border = "#0f172a"
        accent_color = "#00f0ff" # Neon Cyan
        
    img = Image.new("RGB", (WIDTH, HEIGHT), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw simple glowing border
    draw.rectangle([20, 20, WIDTH-20, HEIGHT-20], outline=border_color, width=4)
    draw.rectangle([30, 30, WIDTH-30, HEIGHT-30], outline=inner_border, width=2)
    
    # Load fonts
    try:
        title_font = ImageFont.truetype(FONT_PATH, title_size)
        body_font = ImageFont.truetype(FONT_PATH, body_size)
    except IOError:
        title_font = ImageFont.load_default()
        body_font = ImageFont.load_default()
        
    y_offset = HEIGHT // 2 - 200
    for i, line in enumerate(text_lines):
        if i == 0:
            font = title_font
            color = accent_color
        else:
            font = body_font
            color = "#ffffff" # White
            
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        
        draw.text(((WIDTH - text_w) // 2, y_offset), line, fill=color, font=font)
        y_offset += text_h + 40
        
    out_path = os.path.join(GENERATED_DIR, filename)
    img.save(out_path, "JPEG", quality=95)
    print(f"Created text slide: {out_path}")
    return out_path

# Fallback text slide definitions for legacy insert plans
LEGACY_SLIDES = {
    "history-ai-math-to-model": {
        "ep1": {
            1: ["จากสมการ สู่โมเดล", "", "ต้นกำเนิด AI", "จากเด็กหนุ่มไร้บ้าน"],
            5: ["NO CODE", "", "สมองกลเรียนรู้เครื่องแรก", "ที่ไม่มีสายโค้ดแม้แต่บรรทัดเดียว"],
            8: ["1969", "", "ความตายของ AI", "(AI Winter)"],
            15: ["คณิตศาสตร์ไม่เคยโกหก", "", "มันแค่รอวันที่คอมพิวเตอร์...", "จะตามมันทัน"]
        },
        "ep2": {
            1: ["1969: ยุคมืด ของ AI", "", "และปาฏิหาริย์", "แบคพรอพพาเกชัน"],
            5: ["NO CODE", "", "ไม่มีสายโค้ด", "แม้แต่บรรทัดเดียว"],
            8: ["1986", "", "การคืนชีพที่ถูกซ่อนไว้", "(Backpropagation)"],
            16: ["แคลคูลัสและทฤษฎีเก่าร้อยปี", "", "คือประตูปัญญาประดิษฐ์...", "ที่ถูกเปิดขึ้นใหม่"]
        },
        "ep3": {
            1: ["เมื่อกิกะวัตต์", "", "ปลุกชีพสมการร้อยปี", "ของปัญญาประดิษฐ์"],
            5: ["ชิปการ์ดจอ", "", "และ ข้อมูลมหาศาล", "เชื้อเพลิงสำคัญยุคใหม่"],
            9: ["2012", "", "การปฏิวัติชิปการ์ดจอ", "(The GPU Revolution)"],
            12: ["2017", "", "Attention Is All You Need", "(ทรานส์ฟอร์มเมอร์)"],
            16: ["เมื่อสมการเก่าแก่...", "", "พบกับพลังไฟฟ้าระดับกิกะวัตต์", "ล้านล้านพารามิเตอร์จึงตื่นขึ้น"]
        }
    },
    "brief-history-computer": {
        "ep1": {
            1: ["ประวัติศาสตร์คอมพิวเตอร์", "", "จากฟันเฟือง", "สู่ชิปซิลิคอน"],
            5: ["1837", "", "เครื่องกลวิเคราะห์คณิตศาสตร์", "ของ ชาร์ลส์ แบบเบจ"],
            8: ["1945", "", "ยักษ์ใหญ่ ENIAC", "น้ำหนักกว่า 27 ตัน"],
            11: ["1947", "", "ทรานซิสเตอร์ปฏิวัติวงการ", "ณ เบลล์แล็บส์"],
            14: ["1958", "", "ไมโครชิป", "แผ่นซิลิคอนจิ๋ว"],
            17: ["คอมพิวเตอร์ไม่ได้แค่ย่อขนาด", "", "แต่มันกำลังขยายจินตนาการมนุษย์", "ให้ก้าวไปอย่างไม่มีที่สิ้นสุด"]
        },
        "ep2": {
            1: ["ปฏิวัติพีซี", "", "และโลกอินเทอร์เน็ต", "ของคอมพิวเตอร์"],
            5: ["1977", "", "Apple II คอมพิวเตอร์ส่วนบุคคล", "ที่ใช้งานได้ทันทีจากกล่อง"],
            8: ["1981", "", "IBM PC และ ระบบปฏิบัติการ DOS", "มาตรฐานใหม่ในสำนักงาน"],
            11: ["1984", "", "Macintosh ปฏิวัติกราฟิก UI", "และอุปกรณ์ควบคุมที่เรียกว่า... เมาส์"],
            14: ["1991", "", "กำเนิด World Wide Web", "ชุบชีวิตเครื่องคอมพิวเตอร์ให้เชื่อมต่อกัน"],
            15: ["เครื่องคำนวณในอดีต...", "", "แปรสภาพเป็นประตูบานยักษ์", "เชื่อมโยงความรู้ของมนุษยชาติ"]
        },
        "ep3": {
            1: ["ยุคพกพา", "", "และคลาวด์อัจฉริยะ", "อนาคตของคอมพิวเตอร์"],
            5: ["2007", "", "iPhone ปฏิวัติหน้าจอสัมผัส", "และแอปพลิเคชันยุคใหม่"],
            8: ["2006", "", "การถือกำเนิดของบริการคลาวด์", "พลังงานไฟฟ้าเชิงบริการ"],
            11: ["2010s-2020s", "", "จีพียู และ การเรียนรู้ของจักรกล", "ปลุกชีพปัญญาประดิษฐ์"],
            14: ["ชิปการ์ดจอประมวลผลคู่ขนาน", "", "คีย์สำคัญในการคิด", "และเขียนโปรแกรมได้เอง"],
            15: ["เราได้เปลี่ยนคอมพิวเตอร์...", "", "จากเครื่องช่วยคำนวณ", "ไปสู่... คู่คิดทางปัญญา"]
        }
    }
}

# 1. Parse Insert Plan & Generate Slides
with open(INSERT_PLAN_PATH, "r", encoding="utf-8") as f:
    clips = json.load(f)

text_slides = {}
for i, clip in enumerate(clips):
    idx = i + 1
    # Check if this clip is a text slide
    if clip.get("file") == "text":
        lines = None
        # Try to read custom lines from insert plan first
        if "text_lines" in clip:
            lines = clip["text_lines"]
        # Fall back to legacy registry
        elif slug in LEGACY_SLIDES and episode in LEGACY_SLIDES[slug] and idx in LEGACY_SLIDES[slug][episode]:
            lines = LEGACY_SLIDES[slug][episode][idx]
        
        # If no lines found, split the note description as fallback
        if not lines:
            note_val = clip.get("note", "Text Slide")
            lines = [note_val]
            
        filename = f"temp_text_{idx}.jpg"
        text_slides[idx] = create_text_slide(lines, filename, slug)

# 2. Compile Timeline and Resize Assets
concat_lines = []
print("\nParsing timeline clips:")
for i, clip in enumerate(clips):
    idx = i + 1
    duration = clip["end_sec"] - clip["start_sec"]
    file_val = clip.get("file", "text")
    
    # Resolve image path
    if file_val == "text" or idx in text_slides:
        img_name = f"temp_text_{idx}.jpg"
        img_path = os.path.join(GENERATED_DIR, img_name)
    else:
        base_name = os.path.basename(file_val)
        img_path = os.path.join(GENERATED_DIR, base_name)
        
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Missing visual asset: {img_path}")
        
    # Resize image to 1080x1920
    img = Image.open(img_path)
    if img.size != (WIDTH, HEIGHT):
        img_resized = img.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
        resized_path = os.path.join(SCRATCH_DIR, f"resized_{slug}_{episode}_{idx}.jpg")
        img_resized.save(resized_path, "JPEG", quality=95)
        img_path = resized_path
        
    print(f"  Clip {idx}: {img_path} for {duration:.2f}s")
    
    concat_lines.append(f"file '{img_path}'")
    concat_lines.append(f"duration {duration:.2f}")

# Concat workaround: append last file a second time with a dummy duration
if concat_lines:
    last_file = concat_lines[-2]
    concat_lines.append(last_file)
    concat_lines.append("duration 5.0")

# Write concat list
concat_file_path = os.path.join(SCRATCH_DIR, f"concat_{slug}_{episode}.txt")
with open(concat_file_path, "w", encoding="utf-8") as f:
    f.write("\n".join(concat_lines) + "\n")
print(f"\nWrote concat list to {concat_file_path}")

# Get final target duration (last clip end_sec)
target_sec = clips[-1]["end_sec"]
print(f"Target duration: {target_sec:.2f}s")

# 3. Pad Voiceover Audio to Target Duration
padded_audio_path = os.path.join(SCRATCH_DIR, f"padded_audio_{slug}_{episode}.mp3")
pad_cmd = [
    "ffmpeg", "-y",
    "-i", VOICEOVER_PATH,
    "-f", "lavfi", "-i", "anullsrc",
    "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1[out]",
    "-map", "[out]",
    "-t", f"{target_sec:.2f}",
    padded_audio_path
]
print(f"\nRunning audio padding: {' '.join(pad_cmd)}")
subprocess.run(pad_cmd, check=True, capture_output=True)

# 4. Compile video with FFmpeg
output_video_path = os.path.join(OUT_DIR, f"{episode}.mp4")
ffmpeg_cmd = [
    "ffmpeg", "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", concat_file_path,
    "-i", padded_audio_path,
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-r", "30",
    "-c:a", "aac",
    "-map", "0:v",
    "-map", "1:a",
    "-shortest",
    output_video_path
]

print(f"\nRunning FFmpeg: {' '.join(ffmpeg_cmd)}")
result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)

if result.returncode == 0:
    print(f"\n🎉 Success! Video compiled successfully at: {output_video_path}")
else:
    print(f"\n❌ Error compiling video (Exit Code {result.returncode}):")
    print(result.stderr)
