from quart import Quart, request, jsonify
import QDetect.qdetect as qdetect
from typing import Dict, Any

app = Quart(__name__)
q_annotater = qdetect.qMatcherAnnotater()
SURAH_MAP = {
    "الفاتحة": 1, "البقرة": 2, "آل عمران": 3, "النساء": 4, "المائدة": 5,
    "الأنعام": 6, "الأعراف": 7, "الأنفال": 8, "التوبة": 9, "يونس": 10,
    "هود": 11, "يوسف": 12, "الرعد": 13, "إبراهيم": 14, "الحجر": 15,
    "النحل": 16, "الإسراء": 17, "الكهف": 18, "مريم": 19, "طه": 20,
    "الأنبياء": 21, "الحج": 22, "المؤمنون": 23, "النور": 24, "الفرقان": 25,
    "الشعراء": 26, "النمل": 27, "القصص": 28, "العنكبوت": 29, "الروم": 30,
    "لقمان": 31, "السجدة": 32, "الأحزاب": 33, "سبإ": 34, "فاطر": 35,
    "يس": 36, "الصافات": 37, "ص": 38, "الزمر": 39, "غافر": 40,
    "فصلت": 41, "الشورى": 42, "الزخرف": 43, "الدخان": 44, "الجاثية": 45,
    "الأحقاف": 46, "محمد": 47, "الفتح": 48, "الحجرات": 49, "ق": 50,
    "الذاريات": 51, "الطور": 52, "النجم": 53, "القمر": 54, "الرحمن": 55,
    "الواقعة": 56, "الحديد": 57, "المجادلة": 58, "الحشر": 59, "الممتحنة": 60,
    "الصف": 61, "الجمعة": 62, "المنافقون": 63, "التغابن": 64, "الطلاق": 65,
    "التحريم": 66, "الملك": 67, "القلم": 68, "الحاقة": 69, "المعارج": 70,
    "نوح": 71, "الجن": 72, "المزمل": 73, "المدثر": 74, "القيامة": 75,
    "الإنسان": 76, "المرسلات": 77, "النبأ": 78, "النازعات": 79, "عبس": 80,
    "التكوير": 81, "الانفطار": 82, "المطففين": 83, "الانشقاق": 84, "البروج": 85,
    "الطارق": 86, "الأعلى": 87, "الغاشية": 88, "الفجر": 89, "البلد": 90,
    "الشمس": 91, "الليل": 92, "الضحى": 93, "الشرح": 94, "التين": 95,
    "العلق": 96, "القدر": 97, "البينة": 98, "الزلزلة": 99, "العاديات": 100,
    "القارعة": 101, "التكاثر": 102, "العصر": 103, "الهمزة": 104, "الفيل": 105,
    "قريش": 106, "الماعون": 107, "الكوثر": 108, "الكافرون": 109, "النصر": 110,
    "المسد": 111, "الإخلاص": 112, "الفلق": 113, "الناس": 114
}

# Success response helper
def success_response(data: Dict[str, Any], message: str = "Success") -> tuple:
    return jsonify({"message": message, **data}), 200

# Error response helper
def error_response(message: str, status: int = 400) -> tuple:
    return jsonify({"error": message}), status

@app.route('/')
async def home():
    """Root endpoint returning API status"""
    return success_response({"status": "running"}, "API is running")

@app.route('/docs')
async def docs():
    """Documentation endpoint"""
    return success_response({
        "endpoints": {
            "/": "Returns API status",
            "/docs": "Shows this documentation",
            "/detect_quran": "POST endpoint to detect Quranic content"
        }
    }, "API Documentation")

@app.route('/detect_quran', methods=['POST'])
async def detect_quran():
    """
    Detect Quranic content in provided text
    Expects JSON with 'text' field
    Returns matches with Surah number and Ayah number
    """
    if not request.is_json:
        return error_response("Request must be JSON")

    data = await request.get_json()
    text = data.get('text', '').strip()

    if not text:
        return error_response("Text field is required and cannot be empty")

    # Process text
    matches = q_annotater.matchAll(text)
    count = len(matches)
    
    response_data = {
        "count": count,
        "matches": [
            {"surah_number": SURAH_MAP.get(match["aya_name"], -1), "ayah": match["aya_start"]}
            for match in matches
        ]
    }
    
    return success_response(
        response_data,
        f"Found {count} Quranic reference{'s' if count != 1 else ''}"
    )

if __name__ == '__main__':
    app.run(
        debug=True,
        host='0.0.0.0',
        port=8001,
        use_reloader=True
    )