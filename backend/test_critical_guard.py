from critical_facts import apply_guard, get_critical_answer


def test_location_question_tr():
    answer = get_critical_answer("Selçuk Üniversitesi nerede?", "tr")
    assert answer is not None
    assert "Konya" in answer


def test_location_question_en():
    answer = get_critical_answer("Where is Selcuk University?", "en")
    assert answer is not None
    assert "Konya" in answer


def test_foundation_question_tr():
    answer = get_critical_answer("Selçuk Üniversitesi kaç yılında kuruldu?", "tr")
    assert answer is not None
    assert "1975" in answer


def test_ce_faculty_question_tr():
    answer = get_critical_answer("Bilgisayar Mühendisliği hangi fakültede?", "tr")
    assert answer is not None
    assert "Teknoloji Fakültesi" in answer


def test_address_question_tr():
    answer = get_critical_answer("Selçuk Üniversitesi adresi nedir?", "tr")
    assert answer is not None
    assert "Alaeddin Keykubat Yerleşkesi" in answer


def test_phone_question_tr():
    answer = get_critical_answer("Selçuk Üniversitesi telefon numarası nedir?", "tr")
    assert answer is not None
    assert "+90 332 241 0041" in answer


def test_website_question_tr():
    answer = get_critical_answer("Selçuk Üniversitesi web sitesi nedir?", "tr")
    assert answer is not None
    assert "selcuk.edu.tr" in answer


def test_rector_question_tr():
    answer = get_critical_answer("Selçuk Üniversitesi rektörü kim?", "tr")
    assert answer is not None
    assert "Hüseyin Yılmaz" in answer


def test_student_count_question_tr():
    answer = get_critical_answer("Selçuk Üniversitesi kaç öğrencisi var?", "tr")
    assert answer is not None
    assert "70.000" in answer or "70,000" in answer


def test_academic_units_question_tr():
    answer = get_critical_answer("Selçuk Üniversitesi enstitü sayısı kaç?", "tr")
    assert answer is not None
    assert "7 enstitü" in answer


def test_ce_program_code_question_tr():
    answer = get_critical_answer("Bilgisayar Mühendisliği program kodu nedir?", "tr")
    assert answer is not None
    assert "108911205" in answer


def test_ce_language_question_tr():
    answer = get_critical_answer("Bilgisayar Mühendisliği eğitim dili nedir?", "tr")
    assert answer is not None
    assert "Türkçe" in answer


def test_ce_score_type_question_tr():
    answer = get_critical_answer("Bilgisayar Mühendisliği puan türü nedir?", "tr")
    assert answer is not None
    assert "SAY" in answer


def test_ce_bologna_question_tr():
    answer = get_critical_answer("Bilgisayar Mühendisliği bologna sayfası nedir?", "tr")
    assert answer is not None
    assert "bologna.selcuk.edu.tr" in answer


def test_ce_yokatlas_question_tr():
    answer = get_critical_answer("Bilgisayar Mühendisliği yok atlas linki?", "tr")
    assert answer is not None
    assert "yokatlas.yok.gov.tr" in answer


def test_ce_facebook_question_tr():
    answer = get_critical_answer("Bilgisayar Mühendisliği facebook sayfası?", "tr")
    assert answer is not None
    assert "facebook.com" in answer


def test_non_critical_question():
    answer = get_critical_answer("Selçuk Üniversitesi hakkında genel bilgi verir misin?", "tr")
    assert answer is None


def test_apply_guard_filters_wrong_city():
    raw = "Selçuk Üniversitesi İzmir ve Ankara'da kampüsleri bulunmaktadır."
    answer, guarded = apply_guard("Selçuk Üniversitesi hakkında bilgi ver", raw, "tr")
    assert guarded is True
    assert "İzmir" not in answer
    assert "Ankara" not in answer


def test_apply_guard_keeps_non_selcuk_questions():
    raw = "İzmir, Ege Bölgesi'nde yer alır."
    answer, guarded = apply_guard("İzmir nerede?", raw, "tr")
    assert guarded is False
    assert answer == raw


def test_apply_guard_fallback_when_empty():
    raw = "Selçuk Üniversitesi İzmir'dedir."
    answer, guarded = apply_guard("Selçuk Üniversitesi hakkında bilgi ver", raw, "tr")
    assert guarded is True
    assert "kesin bilgiye sahip değilim" in answer.lower()


def test_apply_guard_filters_wrong_year():
    raw = "Selçuk Üniversitesi 1976 yılında kurulmuştur."
    answer, guarded = apply_guard("Selçuk Üniversitesi hakkında bilgi ver", raw, "tr")
    assert guarded is True
    assert "1976" not in answer
