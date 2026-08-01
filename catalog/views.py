from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from .forms import FoodPhotoAnalysisForm
from .services import (
    FoodAnalysisError,
    analyze_food_image,
    get_gym_exercises,
    get_weekly_training_plans,
)


@login_required
def home(request):
    return render(
        request,
        "home.html",
        {"whatsapp_coach_number": settings.WHATSAPP_COACH_NUMBER},
    )


@login_required
def calorie_calculator(request):
    return render(request, "catalog/calorie_calculator.html")


@login_required
def food_calorie_ai(request):
    form = FoodPhotoAnalysisForm(request.POST or None, request.FILES or None)
    analysis = None
    analysis_error = ""
    api_configured = bool(settings.OPENAI_API_KEY)

    if request.method == "POST" and form.is_valid():
        if not api_configured:
            analysis_error = (
                "ميزة التحليل غير مهيأة بعد. أضف مفتاح OpenAI في إعدادات "
                "الخادم ثم حاول مرة أخرى."
            )
        else:
            now_timestamp = int(timezone.now().timestamp())
            last_analysis = request.session.get("last_food_ai_analysis", 0)
            if now_timestamp - last_analysis < 15:
                analysis_error = (
                    "انتظر بضع ثوانٍ قبل تحليل صورة أخرى لحماية رصيد الخدمة."
                )
            else:
                try:
                    analysis = analyze_food_image(
                        form.cleaned_data["photo"],
                        form.cleaned_data["meal_context"],
                        api_key=settings.OPENAI_API_KEY,
                        model=settings.OPENAI_VISION_MODEL,
                    )
                    request.session["last_food_ai_analysis"] = now_timestamp
                except FoodAnalysisError as error:
                    analysis_error = str(error)

    return render(
        request,
        "catalog/food_calorie_ai.html",
        {
            "form": form,
            "analysis": analysis,
            "analysis_error": analysis_error,
            "api_configured": api_configured,
        },
    )


@login_required
def walking_steps(request):
    return render(request, "catalog/walking_steps.html")


@login_required
def weekly_plan(request):
    plan_days = [
        {
            "number": 1,
            "day": "السبت",
            "focus": "بداية متوازنة",
            "exercise": "تمارين جسم كامل منزلية",
            "exercise_details": (
                "3 جولات: قرفصاء، ضغط، اندفاع أمامي وبلانك، "
                "مع إحماء وتهدئة."
            ),
            "duration": "35 دقيقة",
            "meals": (
                "شوفان بالفواكه للفطور، ودجاج مع الكينوا "
                "والخضروات للغداء، وعشاء خفيف غني بالبروتين."
            ),
            "calories": (
                "التزم بسعرات المحافظة أو هدفك المحسوب، ووزّعها "
                "على 3 وجبات ووجبة خفيفة."
            ),
            "steps": "7,000 خطوة",
            "steps_value": 7000,
        },
        {
            "number": 2,
            "day": "الأحد",
            "focus": "نشاط هوائي",
            "exercise": "مشي سريع وتمارين مرونة",
            "exercise_details": (
                "25 دقيقة مشي سريع، ثم 10 دقائق لتمديد "
                "الساقين والظهر والكتفين."
            ),
            "duration": "35 دقيقة",
            "meals": (
                "توست الأفوكادو والبيض، وشوربة عدس، وطبق "
                "سلطة مع مصدر بروتين مناسب."
            ),
            "calories": (
                "راقب أحجام الحصص والمشروبات؛ اجعل الماء "
                "الخيار الأساسي خلال اليوم."
            ),
            "steps": "8,000 خطوة",
            "steps_value": 8000,
        },
        {
            "number": 3,
            "day": "الاثنين",
            "focus": "الجزء العلوي",
            "exercise": "تمارين صدر وظهر وكتف",
            "exercise_details": (
                "ضغط صدر، سحب أمامي، تجديف بالكابل وضغط كتف؛ "
                "3 جولات بوزن مناسب."
            ),
            "duration": "45 دقيقة",
            "meals": (
                "فطور يحتوي على البيض والحبوب الكاملة، وطبق "
                "سلمون وكينوا، وزبادي طبيعي مع مكسرات."
            ),
            "calories": (
                "وزّع البروتين على الوجبات، وأدخل الوجبات ضمن "
                "ميزانية السعرات اليومية."
            ),
            "steps": "9,000 خطوة",
            "steps_value": 9000,
        },
        {
            "number": 4,
            "day": "الثلاثاء",
            "focus": "تعافٍ نشط",
            "exercise": "مشي مريح وحركة خفيفة",
            "exercise_details": (
                "20 دقيقة مشي مريح مع تمارين حركة للمفاصل "
                "وتنفس هادئ."
            ),
            "duration": "30 دقيقة",
            "meals": (
                "شوفان أو زبادي مع فاكهة، وشوربة عدس، "
                "وخضروات مع بروتين قليل الدهون."
            ),
            "calories": (
                "حافظ على نمطك المعتاد وتجنب خفض الطعام بشدة "
                "في يوم التعافي."
            ),
            "steps": "8,000 خطوة",
            "steps_value": 8000,
        },
        {
            "number": 5,
            "day": "الأربعاء",
            "focus": "الجزء السفلي",
            "exercise": "تمارين الساقين والأرداف",
            "exercise_details": (
                "قرفصاء، رفعة رومانية واندفاع أمامي؛ 3 إلى "
                "4 جولات مع التركيز على التقنية."
            ),
            "duration": "45 دقيقة",
            "meals": (
                "توست أفوكادو وبيض، ودجاج مع الكينوا "
                "والخضروات، وفاكهة مع حفنة مكسرات."
            ),
            "calories": (
                "أعطِ الأولوية للبروتين والكربوهيدرات المعقدة "
                "حول وقت التمرين ضمن هدفك."
            ),
            "steps": "10,000 خطوة",
            "steps_value": 10000,
        },
        {
            "number": 6,
            "day": "الخميس",
            "focus": "لياقة وحركة",
            "exercise": "دائرة تمارين منزلية",
            "exercise_details": (
                "متسلق الجبل، بيربي، قرفصاء وبلانك؛ 30 ثانية "
                "عمل و30 ثانية راحة لأربع جولات."
            ),
            "duration": "30 دقيقة",
            "meals": (
                "وجبات متوازنة تحتوي على خضروات متنوعة، "
                "حبوب كاملة ومصدر بروتين في كل وجبة رئيسية."
            ),
            "calories": (
                "لا تعتبر التمرين مبررًا لتعويض السعرات بكميات "
                "كبيرة؛ التزم بالهدف التقريبي."
            ),
            "steps": "10,000 خطوة",
            "steps_value": 10000,
        },
        {
            "number": 7,
            "day": "الجمعة",
            "focus": "راحة ومراجعة",
            "exercise": "راحة أو نزهة خفيفة",
            "exercise_details": (
                "نزهة مريحة وتمدد بسيط عند الرغبة، مع إعطاء "
                "الأولوية للنوم والتعافي."
            ),
            "duration": "20 دقيقة",
            "meals": (
                "استمتع بوجباتك المعتادة باعتدال، واجعل نصف "
                "الطبق خضروات مع بروتين وحبوب مناسبة."
            ),
            "calories": (
                "راجع متوسط الأسبوع بدل الحكم على وجبة واحدة، "
                "وخطط للأسبوع التالي."
            ),
            "steps": "6,000 خطوة",
            "steps_value": 6000,
        },
    ]

    training_plans = get_weekly_training_plans()
    return render(
        request,
        "catalog/weekly_plan.html",
        {
            "plan_days": plan_days,
            "training_plans": training_plans,
            "home_plan": training_plans[0],
            "gym_plan": training_plans[1],
        },
    )


@login_required
def exercise_list(request):
    exercises = [
        {
            "name": "تمرين الضغط",
            "icon": "💪",
            "image": "images/exercises/push-up.webp",
            "video": "videos/home-push-up-live-side-v3-90s.mp4",
            "narration": [
                "ابدأ بوضع الكفين أسفل الكتفين، ومد جسمك من الرأس حتى الكعبين في خط مستقيم.",
                "شد عضلات البطن والأرداف، ولا تترك الحوض يهبط أثناء الحركة.",
                "اخفض صدرك ببطء، واجعل المرفقين مائلين قليلًا إلى الخلف وقريبين من الجسم.",
                "ازفر وأنت تدفع الأرض للعودة إلى الأعلى، وخذ شهيقًا أثناء النزول.",
                "حافظ على جودة الحركة. إذا صعب التمرين، ضع الركبتين على الأرض وكرر بتحكم.",
            ],
            "location": "home",
            "location_label": "تمرين منزلي",
            "level": "مبتدئ",
            "duration": "10 دقائق",
            "muscles": "الصدر، الكتف، والذراعان",
            "equipment": "لا يحتاج معدات",
            "description": (
                "تمرين أساسي لتقوية الجزء العلوي من الجسم "
                "وتحسين ثبات الجذع."
            ),
            "steps": [
                "ضع الكفين على الأرض بعرض الكتفين ومد الجسم بخط مستقيم.",
                "اخفض صدرك ببطء مع إبقاء المرفقين قريبين من الجسم.",
                "ادفع جسمك للأعلى وكرر 3 جولات، من 8 إلى 12 تكرارًا.",
            ],
        },
        {
            "name": "القرفصاء بوزن الجسم",
            "icon": "🦵",
            "image": "images/exercises/bodyweight-squat-man.webp",
            "video": "videos/home-squat-male-v2-90s.mp4",
            "narration": [
                "قف والقدمان بعرض الكتفين، ووجّه أصابع القدمين إلى الخارج قليلًا.",
                "ابدأ الحركة بدفع الوركين إلى الخلف كأنك تجلس على كرسي.",
                "اثن الركبتين مع إبقائهما في اتجاه أصابع القدمين، وارفع الصدر.",
                "انزل إلى المدى المريح، ثم ادفع الأرض بالكعبين وازفر أثناء الصعود.",
                "لا تضم الركبتين إلى الداخل، وحافظ على ظهر محايد وسرعة متحكم بها.",
            ],
            "location": "home",
            "location_label": "تمرين منزلي",
            "level": "مبتدئ",
            "duration": "12 دقيقة",
            "muscles": "الفخذان والأرداف",
            "equipment": "لا يحتاج معدات",
            "description": (
                "يساعد على تقوية الجزء السفلي من الجسم "
                "وتحسين التوازن والحركة."
            ),
            "steps": [
                "قف والقدمان بعرض الكتفين مع توجيه الصدر للأعلى.",
                "ادفع الوركين للخلف واثن الركبتين حتى وضع مريح.",
                "ارجع للوقوف وكرر 3 جولات، من 12 إلى 15 تكرارًا.",
            ],
        },
        {
            "name": "تمرين البلانك",
            "icon": "⏱️",
            "image": "images/exercises/plank-man.webp",
            "video": "videos/home-plank-male-v2-90s.mp4",
            "narration": [
                "ضع المرفقين مباشرة أسفل الكتفين، واستند إلى الساعدين وأطراف القدمين.",
                "كوّن خطًا مستقيمًا من الرأس إلى الكعبين، وانظر إلى الأرض أمامك قليلًا.",
                "شد البطن والأرداف، واسحب السرة إلى الداخل من دون حبس النفس.",
                "تنفس بهدوء وثبات، واضغط الساعدين في الأرض للمحافظة على وضع الكتفين.",
                "تجنب رفع الحوض أو هبوط أسفل الظهر، وتوقف إذا شعرت بألم حاد.",
            ],
            "location": "home",
            "location_label": "تمرين منزلي",
            "level": "مبتدئ",
            "duration": "8 دقائق",
            "muscles": "البطن وأسفل الظهر",
            "equipment": "بساط تمرين اختياري",
            "description": (
                "تمرين ثبات فعّال لعضلات الجذع يساعد على تحسين "
                "وضعية الجسم."
            ),
            "steps": [
                "استند إلى الساعدين وأطراف القدمين.",
                "حافظ على استقامة الرأس والظهر والساقين.",
                "اثبت من 20 إلى 40 ثانية وكرر 3 مرات.",
            ],
        },
        {
            "name": "تمرين متسلق الجبل",
            "icon": "🏃",
            "image": "images/exercises/mountain-climber.webp",
            "video": "videos/home-mountain-climber-live-v3-90s.mp4",
            "narration": [
                "ابدأ بوضعية الضغط، والكفان أسفل الكتفين والجسم في خط مستقيم.",
                "اسحب ركبة واحدة نحو الصدر، ثم أعدها وبدل بالساق الأخرى.",
                "ثبت الكتفين فوق الكفين، وحافظ على الحوض منخفضًا ومستقرًا.",
                "زد السرعة تدريجيًا مع بقاء الحركة واضحة، وازفر مع سحب كل ركبة.",
                "لا تقفز بعشوائية ولا تقوس أسفل الظهر؛ اختر سرعة تستطيع التحكم بها.",
            ],
            "location": "home",
            "location_label": "تمرين منزلي",
            "level": "متوسط",
            "duration": "15 دقيقة",
            "muscles": "البطن، الكتفين، والساقين",
            "equipment": "لا يحتاج معدات",
            "description": (
                "يجمع بين تمارين القلب وتقوية الجذع لرفع اللياقة "
                "وحرق السعرات."
            ),
            "steps": [
                "ابدأ بوضعية الضغط مع شد عضلات البطن.",
                "اسحب ركبة واحدة نحو الصدر ثم بدّل بين الساقين.",
                "نفّذ 30 ثانية ثم استرح 20 ثانية وكرر 4 جولات.",
            ],
        },
        {
            "name": "الاندفاع الأمامي",
            "icon": "🚶",
            "image": "images/exercises/forward-lunge-man.webp",
            "video": "videos/home-lunge-male-v2-90s.mp4",
            "narration": [
                "قف باستقامة وشد عضلات البطن، ثم تقدم خطوة واسعة إلى الأمام.",
                "اخفض جسمك رأسيًا حتى تقترب الركبتان من زاوية تسعين درجة.",
                "اجعل الركبة الأمامية في اتجاه القدم، وأبق الصدر مرفوعًا والظهر محايدًا.",
                "ادفع بالكعب الأمامي للعودة إلى الوقوف، ثم بدل الساق مع الزفير.",
                "حافظ على التوازن ولا تدع الركبة تنهار للداخل، واستخدم وزن الجسم للمبتدئ.",
            ],
            "location": "home",
            "location_label": "تمرين منزلي",
            "level": "متوسط",
            "duration": "12 دقيقة",
            "muscles": "الفخذان والأرداف",
            "equipment": "لا يحتاج معدات",
            "description": (
                "يقوي كل ساق بصورة منفردة ويساعد على تحسين "
                "الثبات والتناسق."
            ),
            "steps": [
                "قف باستقامة ثم تقدم خطوة واسعة إلى الأمام.",
                "اخفض الركبة الخلفية مع بقاء الأمامية فوق الكاحل.",
                "ادفع بالقدم الأمامية وبدّل الساق؛ 10 تكرارات لكل ساق.",
            ],
        },
        {
            "name": "تمرين بيربي",
            "icon": "🔥",
            "image": "images/exercises/burpee.webp",
            "video": "videos/home-burpee-male-v2-90s.mp4",
            "narration": [
                "ابدأ واقفًا، ثم انزل إلى القرفصاء وضع الكفين على الأرض أمام القدمين.",
                "أعد القدمين إلى الخلف لتصل إلى وضعية الضغط مع شد عضلات البطن.",
                "نفذ تمرين ضغط اختياريًا، ثم أعد القدمين قرب الكفين بحركة متحكم بها.",
                "اصعد واقفز إلى الأعلى، ثم اهبط برفق على منتصف القدم واثن الركبتين.",
                "حافظ على إيقاع مناسب؛ ويمكنك الرجوع بالقدمين خطوة خطوة لتخفيف الشدة.",
            ],
            "location": "home",
            "location_label": "تمرين منزلي",
            "level": "متقدم",
            "duration": "15 دقيقة",
            "muscles": "الجسم كاملًا",
            "equipment": "لا يحتاج معدات",
            "description": (
                "تمرين عالي الشدة يرفع نبض القلب ويشغّل معظم "
                "عضلات الجسم."
            ),
            "steps": [
                "انزل إلى القرفصاء وضع كفيك على الأرض.",
                "اقفز بالقدمين للخلف إلى وضعية الضغط ثم أعدهما.",
                "اقفز للأعلى وكرر 3 جولات، من 8 إلى 10 تكرارات.",
            ],
        },
        *get_gym_exercises(),
    ]

    return render(
        request,
        "catalog/exercise_list.html",
        {"exercises": exercises},
    )


@login_required
def healthy_food_list(request):
    nutrition_items = [
        {
            "name": "طبق السلمون والكينوا",
            "icon": "🐟",
            "image": "images/nutrition/salmon-quinoa-bowl.webp",
            "category": "food",
            "subcategory": "fish",
            "subcategory_label": "أسماك",
            "category_label": "وجبة صحية",
            "summary": (
                "سلمون مشوي مع الكينوا والأفوكادو والخضروات "
                "الطازجة."
            ),
            "ingredients": (
                "سلمون، كينوا، أفوكادو، خيار، طماطم، "
                "خضروات ورقية وليمون"
            ),
            "benefits": [
                "يوفر بروتينًا عالي الجودة يساعد في بناء وصيانة العضلات.",
                "يحتوي السلمون على دهون أوميغا 3 المفيدة لصحة القلب.",
                "تضيف الكينوا والخضروات أليافًا تدعم الشبع والهضم.",
            ],
        },
        {
            "name": "شوفان بالفواكه والمكسرات",
            "icon": "🥣",
            "image": "images/nutrition/oatmeal-berries.webp",
            "category": "food",
            "subcategory": "vegetarian",
            "subcategory_label": "وجبات نباتية ومتنوعة",
            "category_label": "وجبة صحية",
            "summary": (
                "فطور دافئ من الشوفان مع التوت والموز والجوز "
                "وبذور الشيا."
            ),
            "ingredients": (
                "شوفان، توت، فراولة، موز، جوز، بذور الشيا "
                "وقرفة"
            ),
            "benefits": [
                "الشوفان مصدر للألياف القابلة للذوبان التي تدعم الشبع.",
                "الفواكه تضيف فيتامينات ومركبات نباتية متنوعة.",
                "المكسرات والبذور توفر دهونًا غير مشبعة وبعض البروتين.",
            ],
        },
        {
            "name": "دجاج مشوي مع الكينوا",
            "icon": "🍗",
            "image": "images/nutrition/chicken-quinoa-plate.webp",
            "category": "food",
            "subcategory": "chicken",
            "subcategory_label": "دجاج",
            "category_label": "وجبة صحية",
            "summary": (
                "وجبة متوازنة من الدجاج المشوي والكينوا "
                "والخضروات الملونة."
            ),
            "ingredients": (
                "صدر دجاج، كينوا، بروكلي، فلفل، كوسة، "
                "سلطة ورقية وليمون"
            ),
            "benefits": [
                "يوفر الدجاج بروتينًا قليل الدهون عند تحضيره دون جلد.",
                "تجمع الوجبة بين البروتين والكربوهيدرات المعقدة والخضروات.",
                "تنوع ألوان الخضروات يزيد تنوع العناصر الغذائية.",
            ],
        },
        {
            "name": "توست الأفوكادو والبيض",
            "icon": "🥑",
            "image": "images/nutrition/avocado-egg-toast.webp",
            "category": "food",
            "subcategory": "vegetarian",
            "subcategory_label": "وجبات نباتية ومتنوعة",
            "category_label": "وجبة صحية",
            "summary": (
                "خبز حبوب كاملة مع الأفوكادو والبيض المسلوق "
                "والطماطم."
            ),
            "ingredients": (
                "خبز حبوب كاملة، أفوكادو، بيض، طماطم، "
                "براعم وبذور سمسم"
            ),
            "benefits": [
                "البيض مصدر للبروتين وعدد من الفيتامينات والمعادن.",
                "يوفر الأفوكادو دهونًا غير مشبعة وأليافًا.",
                "خبز الحبوب الكاملة يساعد على زيادة تناول الألياف.",
            ],
        },
        {
            "name": "شوربة العدس",
            "icon": "🍲",
            "image": "images/nutrition/lentil-soup.webp",
            "category": "food",
            "subcategory": "vegetarian",
            "subcategory_label": "وجبات نباتية ومتنوعة",
            "category_label": "وجبة صحية",
            "summary": (
                "شوربة دافئة وغنية بالعدس الأحمر مع الكمون "
                "والليمون."
            ),
            "ingredients": (
                "عدس أحمر، بصل، جزر، طماطم، كمون، بقدونس "
                "وليمون"
            ),
            "benefits": [
                "العدس مصدر نباتي جيد للبروتين والحديد.",
                "محتواه من الألياف يساعد على الشبع وانتظام الهضم.",
                "يمكن أن تكون وجبة مغذية وقليلة الدهون المشبعة.",
            ],
        },
        {
            "name": "سلطة التونة والحمص",
            "icon": "🥗",
            "image": "images/nutrition/tuna-chickpea-salad.webp",
            "category": "food",
            "subcategory": "fish",
            "subcategory_label": "أسماك",
            "category_label": "وجبة صحية",
            "summary": (
                "سلطة مشبعة تجمع التونة والحمص مع الخضروات "
                "الطازجة وتتبيلة الليمون."
            ),
            "ingredients": (
                "تونة، حمص، خيار، طماطم كرزية، بصل أحمر، "
                "بقدونس، ليمون وزيت زيتون"
            ),
            "benefits": [
                "تجمع بين البروتين الحيواني والنباتي في وجبة واحدة.",
                "يوفر الحمص والخضروات أليافًا تساعد على الشبع.",
                "يمكن تحضيرها سريعًا وتناولها كغداء خفيف ومتوازن.",
            ],
        },
        {
            "name": "لفائف الدجاج والخضروات",
            "icon": "🌯",
            "image": "images/nutrition/chicken-vegetable-wrap.webp",
            "category": "food",
            "subcategory": "chicken",
            "subcategory_label": "دجاج",
            "category_label": "وجبة صحية",
            "summary": (
                "خبز حبوب كاملة محشو بالدجاج المشوي والخضروات "
                "مع صلصة زبادي خفيفة."
            ),
            "ingredients": (
                "خبز حبوب كاملة، صدر دجاج، خس، طماطم، فلفل ملون "
                "وزبادي طبيعي"
            ),
            "benefits": [
                "يوفر الدجاج بروتينًا يدعم صيانة الكتلة العضلية.",
                "تضيف الخضروات ألوانًا وعناصر غذائية متنوعة.",
                "خبز الحبوب الكاملة يرفع محتوى الوجبة من الألياف.",
            ],
        },
        {
            "name": "زبادي يوناني بالفواكه والمكسرات",
            "icon": "🫐",
            "image": "images/nutrition/greek-yogurt-fruit-bowl.webp",
            "category": "food",
            "subcategory": "vegetarian",
            "subcategory_label": "وجبات نباتية ومتنوعة",
            "category_label": "وجبة صحية",
            "summary": (
                "وعاء زبادي يوناني كريمي مع التوت والموز والمكسرات "
                "وبذور الشيا."
            ),
            "ingredients": (
                "زبادي يوناني، توت، فراولة، موز، لوز، جوز "
                "وبذور الشيا"
            ),
            "benefits": [
                "الزبادي اليوناني غني بالبروتين ويحتوي على الكالسيوم.",
                "تضيف الفواكه فيتامينات ونكهة حلوة طبيعية.",
                "توفر المكسرات والبذور دهونًا غير مشبعة وأليافًا.",
            ],
        },
        {
            "name": "الشاي الأخضر",
            "icon": "🍵",
            "image": "images/nutrition/green-tea.webp",
            "category": "drink",
            "subcategory": "healthy_drink",
            "subcategory_label": "مشروبات صحية",
            "category_label": "مشروب صحي",
            "summary": (
                "شاي أخضر دافئ دون سكر مضاف، مناسب كمشروب "
                "خفيف خلال اليوم."
            ),
            "ingredients": "ماء وأوراق شاي أخضر",
            "benefits": [
                "يساهم في تناول السوائل عند شربه دون سكر مضاف.",
                "يحتوي على مركبات نباتية مضادة للأكسدة.",
                "بديل منخفض السعرات للمشروبات المحلاة.",
            ],
        },
        {
            "name": "السموذي الأخضر",
            "icon": "🥤",
            "image": "images/nutrition/green-smoothie.webp",
            "category": "drink",
            "subcategory": "healthy_drink",
            "subcategory_label": "مشروبات صحية",
            "category_label": "مشروب صحي",
            "summary": (
                "سموذي كثيف من السبانخ والموز والتفاح والخيار "
                "والزبادي."
            ),
            "ingredients": (
                "سبانخ، موز، تفاح أخضر، خيار، زبادي طبيعي "
                "وماء"
            ),
            "benefits": [
                "يضيف الخضروات والفاكهة إلى الوجبة بطريقة سهلة.",
                "الزبادي يضيف البروتين والكالسيوم بحسب النوع المستخدم.",
                "الاحتفاظ باللب يساعد على بقاء جزء أكبر من الألياف.",
            ],
        },
        {
            "name": "ماء الليمون والخيار والنعناع",
            "icon": "💧",
            "image": "images/nutrition/lemon-mint-water.webp",
            "category": "drink",
            "subcategory": "healthy_drink",
            "subcategory_label": "مشروبات صحية",
            "category_label": "مشروب صحي",
            "summary": (
                "ماء بارد منقوع بشرائح الليمون والخيار "
                "وأوراق النعناع."
            ),
            "ingredients": "ماء، ليمون، خيار، نعناع وثلج",
            "benefits": [
                "يساعد على الترطيب مثل الماء العادي مع نكهة طبيعية.",
                "قد يشجع من لا يفضل الماء العادي على شرب كمية أكبر.",
                "بديل خالٍ من السكر للمشروبات الغازية والمحلاة.",
            ],
        },
        {
            "name": "عصير البرتقال والجزر",
            "icon": "🥕",
            "image": "images/nutrition/orange-carrot-juice.webp",
            "category": "drink",
            "subcategory": "healthy_drink",
            "subcategory_label": "مشروبات صحية",
            "category_label": "مشروب صحي",
            "summary": (
                "عصير طازج من البرتقال والجزر مع لمسة بسيطة "
                "من الزنجبيل."
            ),
            "ingredients": "برتقال، جزر وقطعة صغيرة من الزنجبيل",
            "benefits": [
                "يوفر فيتامين C وبيتا كاروتين من مكوناته الطبيعية.",
                "يمكن أن يضيف تنوعًا للنظام الغذائي عند تناوله باعتدال.",
                "تحضيره دون سكر مضاف أفضل من كثير من العصائر الجاهزة.",
            ],
        },
        {
            "name": "شاي الكركديه",
            "icon": "🌺",
            "image": "images/nutrition/hibiscus-tea.webp",
            "category": "drink",
            "subcategory": "healthy_drink",
            "subcategory_label": "مشروبات صحية",
            "category_label": "مشروب صحي",
            "summary": (
                "منقوع كركديه منعش يمكن تقديمه باردًا أو دافئًا "
                "دون سكر."
            ),
            "ingredients": "ماء وزهور كركديه مجففة",
            "benefits": [
                "مشروب عشبي خالٍ من الكافيين بطبيعته.",
                "يوفر نكهة قوية دون الحاجة إلى إضافة السكر.",
                "يساهم في تنويع مصادر السوائل خلال اليوم.",
            ],
        },
        {
            "name": "سموذي التوت والزبادي",
            "icon": "🫐",
            "image": "images/nutrition/berry-yogurt-smoothie.webp",
            "category": "drink",
            "subcategory": "healthy_drink",
            "subcategory_label": "مشروبات صحية",
            "category_label": "مشروب صحي",
            "summary": (
                "سموذي كريمي من التوت والزبادي والموز دون حاجة "
                "إلى سكر مضاف."
            ),
            "ingredients": (
                "توت مشكل، زبادي طبيعي، نصف موزة، حليب أو ماء "
                "وبذور شيا"
            ),
            "benefits": [
                "يوفر مزيجًا من البروتين والكربوهيدرات من مكوناته.",
                "التوت يضيف مركبات نباتية وفيتامينات متنوعة.",
                "الاحتفاظ بالفاكهة كاملة يحافظ على ألياف أكثر من تصفيتها.",
            ],
        },
        {
            "name": "شاي الزنجبيل والليمون",
            "icon": "🫚",
            "image": "images/nutrition/ginger-lemon-tea.webp",
            "category": "drink",
            "subcategory": "healthy_drink",
            "subcategory_label": "مشروبات صحية",
            "category_label": "مشروب صحي",
            "summary": (
                "منقوع دافئ وعطري من شرائح الزنجبيل والليمون "
                "والنعناع."
            ),
            "ingredients": "ماء، زنجبيل طازج، ليمون وأوراق نعناع",
            "benefits": [
                "يساهم في تناول السوائل دون إضافة السكر.",
                "يمنح الزنجبيل والليمون المشروب نكهة قوية وطبيعية.",
                "بديل دافئ وخفيف للمشروبات المحلاة خلال اليوم.",
            ],
        },
        {
            "name": "لبن بالخيار والنعناع",
            "icon": "🥛",
            "image": "images/nutrition/cucumber-mint-laban.webp",
            "category": "drink",
            "subcategory": "healthy_drink",
            "subcategory_label": "مشروبات صحية",
            "category_label": "مشروب صحي",
            "summary": (
                "مشروب لبن بارد ومنعش ممزوج بالخيار والنعناع "
                "وقليل من الثلج."
            ),
            "ingredients": "لبن طبيعي، خيار، نعناع، ماء بارد وثلج",
            "benefits": [
                "يوفر اللبن البروتين والكالسيوم بحسب النوع المستخدم.",
                "يساعد تقديمه باردًا على إضافة خيار منعش مع الوجبات.",
                "يمكن تقليل الصوديوم باختيار لبن غير مملح.",
            ],
        },
        {
            "name": "شرائح اللحم قليلة الدهون",
            "icon": "🥩",
            "image": "images/nutrition/lean-beef-steak.webp",
            "category": "food",
            "subcategory": "meat",
            "subcategory_label": "لحوم قليلة الدهون",
            "category_label": "وجبة صحية",
            "summary": (
                "شرائح لحم بقري مشوية مع البطاطا الحلوة "
                "والبروكلي في طبق متوازن."
            ),
            "ingredients": (
                "قطعة لحم بقري قليلة الدهون، بطاطا حلوة، "
                "بروكلي، أعشاب وليمون"
            ),
            "benefits": [
                "يوفر اللحم البروتين والحديد والزنك.",
                "اختيار القطع قليلة الدهون يساعد على تقليل الدهون المشبعة.",
                "تضيف الخضروات والبطاطا الحلوة أليافًا وكربوهيدرات متنوعة.",
            ],
        },
        {
            "name": "كفتة لحم مشوية مع الأرز البني",
            "icon": "🍢",
            "image": "images/nutrition/lean-beef-kofta.webp",
            "category": "food",
            "subcategory": "meat",
            "subcategory_label": "لحوم قليلة الدهون",
            "category_label": "وجبة صحية",
            "summary": (
                "كفتة لحم مشوية مع الأرز البني والسلطة "
                "وصلصة زبادي خفيفة."
            ),
            "ingredients": (
                "لحم مفروم قليل الدهون، بقدونس، بهارات، أرز بني، "
                "خيار، طماطم وزبادي"
            ),
            "benefits": [
                "تقدم وجبة غنية بالبروتين مع حصة واضحة من الحبوب والخضروات.",
                "الشواء يقلل الحاجة إلى كميات كبيرة من الزيت.",
                "يمكن خفض الصوديوم باستخدام بهارات وأعشاب بدل الملح الزائد.",
            ],
        },
        {
            "name": "مياه غازية بالليمون والنعناع",
            "icon": "🫧",
            "image": "images/nutrition/sparkling-lemon-mint.webp",
            "category": "drink",
            "subcategory": "carbonated",
            "subcategory_label": "مشروبات غازية مناسبة",
            "category_label": "مشروب غازي دون سكر",
            "serving_note": "مناسب مع الوجبة عند تحضيره دون سكر مضاف.",
            "summary": (
                "مياه غازية منعشة بشرائح الليمون والنعناع "
                "كبديل للمشروبات الغازية المحلاة."
            ),
            "ingredients": "مياه غازية، ليمون، نعناع وثلج",
            "benefits": [
                "يوفر ترطيبًا دون سكر أو سعرات عند عدم إضافة المحليات.",
                "الليمون والنعناع يضيفان نكهة طبيعية واضحة.",
                "خيار مناسب مع الوجبات لمن يفضل الإحساس الغازي.",
            ],
        },
        {
            "name": "مياه غازية بالتوت والليمون الأخضر",
            "icon": "🍓",
            "image": "images/nutrition/sparkling-berry-lime.webp",
            "category": "drink",
            "subcategory": "carbonated",
            "subcategory_label": "مشروبات غازية مناسبة",
            "category_label": "مشروب غازي دون سكر",
            "serving_note": "استخدم الفاكهة للنكهة دون إضافة شراب سكري.",
            "summary": (
                "مياه فوارة بالتوت وشرائح الليمون الأخضر، "
                "تقدم باردة مع الوجبة."
            ),
            "ingredients": (
                "مياه غازية، توت مشكل، ليمون أخضر، نعناع وثلج"
            ),
            "benefits": [
                "بديل غير محلى للمشروبات الغازية التقليدية.",
                "تضيف الفاكهة رائحة ونكهة دون الحاجة إلى شراب مركز.",
                "يساعد تنويع نكهة الماء بعض الأشخاص على زيادة تناول السوائل.",
            ],
        },
        {
            "name": "مشروب غازي خالٍ من السكر",
            "icon": "🥤",
            "image": "images/nutrition/zero-sugar-cola.webp",
            "category": "drink",
            "subcategory": "carbonated",
            "subcategory_label": "مشروبات غازية مناسبة",
            "category_label": "خيار عرضي خالٍ من السكر",
            "serving_note": "خيار عرضي مع الوجبة؛ الماء يبقى المشروب الأساسي.",
            "summary": (
                "خيار غازي خالٍ من السكر يمكن إدخاله باعتدال "
                "عند الرغبة في مشروب بنكهة الكولا."
            ),
            "ingredients": (
                "مياه غازية، نكهات وملونات غذائية، محليات غير سكرية، "
                "وقد يحتوي على الكافيين"
            ),
            "benefits": [
                "لا يضيف السكر عند اختيار منتج يحمل بوضوح عبارة خالٍ من السكر.",
                "قد يكون بديلًا عرضيًا لمن يريد تقليل المشروبات المحلاة.",
                "يفضل الانتباه للكافيين وعدم اعتباره بديلًا يوميًا للماء.",
            ],
        },
    ]

    nutrition_categories = [
        {
            "slug": "food",
            "label": "جميع الوجبات",
            "icon": "🥗",
            "count": sum(
                item["category"] == "food"
                for item in nutrition_items
            ),
        },
        {
            "slug": "drink",
            "label": "جميع المشروبات",
            "icon": "🥤",
            "count": sum(
                item["category"] == "drink"
                for item in nutrition_items
            ),
        },
    ]
    nutrition_items.sort(
        key=lambda item: 0 if item["category"] == "food" else 1
    )

    return render(
        request,
        "catalog/healthy_food_list.html",
        {
            "nutrition_items": nutrition_items,
            "nutrition_categories": nutrition_categories,
        },
    )
