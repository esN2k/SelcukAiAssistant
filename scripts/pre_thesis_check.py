"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  DOSYA ADI: scripts/pre_thesis_check.py                                       ║
║  AMAÇ: Tez sunumu öncesi otomatik kontrol scripti                             ║
║  KULLANIM: python scripts/pre_thesis_check.py                                 ║
║  BAĞIMLILIKLAR: pathlib, ast, subprocess                                       ║
║  YAZAN: esN2k - Selçuk Üniversitesi                                           ║
╚════════════════════════════════════════════════════════════════════════════════╝

DETAYLI AÇIKLAMA:
─────────────────
Bu script, projenin tez sunumuna hazır olup olmadığını kontrol eder.

KONTROL KATEGORİLERİ:
1. Kod Kalitesi: Docstring, type hints, linting
2. Dokümantasyon: README dosyaları, API docs
3. Testler: Coverage, başarı oranı
4. Performans: Benchmark sonuçları
5. Güvenlik: Hassas veri kontrolü
6. Deployment: Gerekli dosyalar

ÇIKTI:
- ✅ Tüm kontroller başarılı → "PROJE TEZ SUNUMUNA HAZIR!"
- ⚠️ Eksikler var → Detaylı rapor ve düzeltme önerileri
"""
import ast
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Renkli çıktı için ANSI kodları
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text: str):
    """Başlık yazdır."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(70)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")

def print_success(text: str):
    """Başarı mesajı yazdır."""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_warning(text: str):
    """Uyarı mesajı yazdır."""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_error(text: str):
    """Hata mesajı yazdır."""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_info(text: str):
    """Bilgi mesajı yazdır."""
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")


class ThesisChecker:
    """Tez hazırlık kontrol sınıfı."""
    
    def __init__(self, repo_path: Path):
        """
        Checker'ı başlat.
        
        Args:
            repo_path: Repository kök dizini
        """
        self.repo_path = repo_path
        self.backend_path = repo_path / "backend"
        self.frontend_path = repo_path / "lib"
        self.docs_path = repo_path / "docs"
        self.results: Dict[str, bool] = {}
        
    def run_all_checks(self) -> bool:
        """
        Tüm kontrolleri çalıştır.
        
        Returns:
            bool: Tüm kontroller başarılı mı?
        """
        print_header("🔍 TEZ HAZIRLIK KONTROLÜ BAŞLIYOR")
        
        checks = [
            ("Kod Kalitesi", self.check_code_quality),
            ("Dokümantasyon", self.check_documentation),
            ("Testler", self.check_tests),
            ("Performans", self.check_performance),
            ("Güvenlik", self.check_security),
            ("Deployment", self.check_deployment),
        ]
        
        for check_name, check_func in checks:
            print_header(f"📋 {check_name} Kontrolü")
            try:
                result = check_func()
                self.results[check_name] = result
            except Exception as e:
                print_error(f"Kontrol hatası: {e}")
                self.results[check_name] = False
        
        return self.print_summary()
    
    def check_code_quality(self) -> bool:
        """Kod kalitesi kontrolü."""
        all_passed = True
        
        # 1. Python dosyalarında docstring kontrolü
        print_info("Python dosyalarında docstring kontrolü...")
        missing_docstrings = self._check_python_docstrings()
        
        if missing_docstrings:
            print_warning(f"{len(missing_docstrings)} dosyada docstring eksik:")
            for file, missing in missing_docstrings[:5]:  # İlk 5'i göster
                print(f"  - {file}: {', '.join(missing[:3])}")
            if len(missing_docstrings) > 5:
                print(f"  ... ve {len(missing_docstrings) - 5} dosya daha")
            all_passed = False
        else:
            print_success("Tüm Python dosyalarında docstring mevcut")
        
        # 2. Type hints kontrolü
        print_info("Type hints kontrolü...")
        files_without_types = self._check_type_hints()
        
        if files_without_types:
            print_warning(f"{len(files_without_types)} dosyada type hints eksik")
            all_passed = False
        else:
            print_success("Type hints kullanımı yeterli")
        
        # 3. Linting kontrolü (ruff varsa)
        print_info("Linting kontrolü...")
        try:
            result = subprocess.run(
                ["ruff", "check", str(self.backend_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                print_success("Linting temiz (ruff)")
            else:
                print_warning("Linting uyarıları var")
                all_passed = False
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print_info("Ruff bulunamadı, linting atlandı")
        
        return all_passed
    
    def _check_python_docstrings(self) -> List[Tuple[str, List[str]]]:
        """Python dosyalarında docstring kontrolü."""
        missing = []
        
        for py_file in self.backend_path.rglob("*.py"):
            # venv ve __pycache__ atla
            if "venv" in str(py_file) or "__pycache__" in str(py_file):
                continue
            
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    tree = ast.parse(f.read())
                
                missing_items = []
                
                # Modül docstring
                if not ast.get_docstring(tree):
                    missing_items.append("module")
                
                # Fonksiyon ve sınıf docstringleri
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        if not ast.get_docstring(node) and not node.name.startswith("_"):
                            missing_items.append(f"function:{node.name}")
                    elif isinstance(node, ast.ClassDef):
                        if not ast.get_docstring(node):
                            missing_items.append(f"class:{node.name}")
                
                if missing_items:
                    missing.append((str(py_file.relative_to(self.repo_path)), missing_items))
            
            except Exception as e:
                print_warning(f"Dosya okunamadı: {py_file} - {e}")
        
        return missing
    
    def _check_type_hints(self) -> List[str]:
        """Type hints kontrolü."""
        files_without_types = []
        
        for py_file in self.backend_path.rglob("*.py"):
            if "venv" in str(py_file) or "__pycache__" in str(py_file):
                continue
            
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                # Basit kontrol: -> ve : var mı?
                if "def " in content and "->" not in content and ": " not in content:
                    files_without_types.append(str(py_file.relative_to(self.repo_path)))
            
            except Exception:
                pass
        
        return files_without_types
    
    def check_documentation(self) -> bool:
        """Dokümantasyon kontrolü."""
        all_passed = True
        
        # 1. Ana README kontrolü
        print_info("Ana README kontrolü...")
        main_readme = self.repo_path / "README.md"
        if main_readme.exists() and main_readme.stat().st_size > 1000:
            print_success("Ana README mevcut ve detaylı")
        else:
            print_error("Ana README eksik veya yetersiz")
            all_passed = False
        
        # 2. Klasör README'leri
        print_info("Klasör README kontrolü...")
        required_readmes = [
            self.backend_path / "README.md",
            self.backend_path / "providers" / "README.md",
            self.backend_path / "services" / "README.md",
            self.docs_path / "README.md",
        ]
        
        missing_readmes = [r for r in required_readmes if not r.exists()]
        
        if missing_readmes:
            print_warning(f"{len(missing_readmes)} klasörde README eksik:")
            for readme in missing_readmes:
                print(f"  - {readme.relative_to(self.repo_path)}")
            all_passed = False
        else:
            print_success("Tüm önemli klasörlerde README mevcut")
        
        # 3. Tez sunumu dokümanı
        print_info("Tez sunumu dokümanı kontrolü...")
        thesis_doc = self.docs_path / "THESIS_PRESENTATION.md"
        if thesis_doc.exists() and thesis_doc.stat().st_size > 5000:
            print_success("Tez sunumu dokümanı hazır")
        else:
            print_error("Tez sunumu dokümanı eksik")
            all_passed = False
        
        return all_passed
    
    def check_tests(self) -> bool:
        """Test kontrolü."""
        all_passed = True
        
        # 1. Test dosyaları var mı?
        print_info("Test dosyaları kontrolü...")
        test_files = list((self.backend_path / "tests").rglob("test_*.py")) if (self.backend_path / "tests").exists() else []
        
        if len(test_files) < 3:
            print_warning(f"Sadece {len(test_files)} test dosyası bulundu")
            all_passed = False
        else:
            print_success(f"{len(test_files)} test dosyası mevcut")
        
        # 2. Pytest çalıştır (varsa)
        print_info("Testleri çalıştırma...")
        try:
            result = subprocess.run(
                ["pytest", str(self.backend_path / "tests"), "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(self.backend_path)
            )
            
            if result.returncode == 0:
                print_success("Tüm testler başarılı")
            else:
                print_warning("Bazı testler başarısız")
                # Başarısız testleri göster
                if "FAILED" in result.stdout:
                    failed_tests = [line for line in result.stdout.split("\n") if "FAILED" in line]
                    print(f"  Başarısız: {len(failed_tests)} test")
                all_passed = False
        
        except FileNotFoundError:
            print_info("Pytest bulunamadı, testler atlandı")
        except subprocess.TimeoutExpired:
            print_warning("Testler zaman aşımına uğradı")
            all_passed = False
        
        return all_passed
    
    def check_performance(self) -> bool:
        """Performans kontrolü."""
        all_passed = True
        
        print_info("Performans metrikleri kontrolü...")
        
        # Benchmark dosyası var mı?
        benchmark_file = self.docs_path / "BENCHMARK_RAPORU.md"
        if benchmark_file.exists():
            print_success("Benchmark raporu mevcut")
        else:
            print_warning("Benchmark raporu eksik")
            all_passed = False
        
        # Test sonuçları var mı?
        test_results = self.docs_path / "TEST_RESULTS.md"
        if test_results.exists():
            print_success("Test sonuçları dokümante edilmiş")
        else:
            print_warning("Test sonuçları dokümantasyonu eksik")
            all_passed = False
        
        return all_passed
    
    def check_security(self) -> bool:
        """Güvenlik kontrolü."""
        all_passed = True
        
        print_info("Hassas veri kontrolü...")
        
        # .env dosyası git'te mi?
        gitignore = self.repo_path / ".gitignore"
        if gitignore.exists():
            with open(gitignore, "r") as f:
                content = f.read()
                if ".env" in content:
                    print_success(".env dosyası .gitignore'da")
                else:
                    print_error(".env dosyası .gitignore'da değil!")
                    all_passed = False
        else:
            print_error(".gitignore dosyası yok!")
            all_passed = False
        
        # API anahtarları hardcoded mı?
        print_info("Hardcoded API anahtarı kontrolü...")
        suspicious_patterns = ["api_key =", "API_KEY =", "secret =", "password ="]
        suspicious_files = []
        
        for py_file in self.backend_path.rglob("*.py"):
            if "venv" in str(py_file):
                continue
            
            try:
                with open(py_file, "r", encoding="utf-8") as f:
                    content = f.read().lower()
                    for pattern in suspicious_patterns:
                        if pattern.lower() in content and "os.getenv" not in content:
                            suspicious_files.append(str(py_file.relative_to(self.repo_path)))
                            break
            except Exception:
                pass
        
        if suspicious_files:
            print_warning(f"{len(suspicious_files)} dosyada hardcoded secret olabilir:")
            for file in suspicious_files[:3]:
                print(f"  - {file}")
            all_passed = False
        else:
            print_success("Hardcoded secret bulunamadı")
        
        return all_passed
    
    def check_deployment(self) -> bool:
        """Deployment hazırlık kontrolü."""
        all_passed = True
        
        print_info("Deployment dosyaları kontrolü...")
        
        # requirements.txt
        requirements = self.backend_path / "requirements.txt"
        if requirements.exists() and requirements.stat().st_size > 100:
            print_success("requirements.txt mevcut")
        else:
            print_error("requirements.txt eksik veya boş")
            all_passed = False
        
        # .env.example
        env_example = self.backend_path / ".env.example"
        if env_example.exists():
            print_success(".env.example mevcut")
        else:
            print_warning(".env.example eksik")
            all_passed = False
        
        # Docker dosyaları (opsiyonel)
        dockerfile = self.repo_path / "Dockerfile"
        docker_compose = self.repo_path / "docker-compose.yml"
        
        if dockerfile.exists() or docker_compose.exists():
            print_success("Docker yapılandırması mevcut")
        else:
            print_info("Docker yapılandırması yok (opsiyonel)")
        
        return all_passed
    
    def print_summary(self) -> bool:
        """Özet rapor yazdır."""
        print_header("📊 ÖZET RAPOR")
        
        total = len(self.results)
        passed = sum(1 for v in self.results.values() if v)
        failed = total - passed
        
        print(f"\nToplam Kontrol: {total}")
        print(f"{Colors.GREEN}Başarılı: {passed}{Colors.END}")
        print(f"{Colors.RED}Başarısız: {failed}{Colors.END}")
        print(f"\nBaşarı Oranı: {(passed/total)*100:.1f}%\n")
        
        # Detaylı sonuçlar
        for check_name, result in self.results.items():
            if result:
                print_success(f"{check_name}: BAŞARILI")
            else:
                print_error(f"{check_name}: BAŞARISIZ")
        
        # Final karar
        print("\n" + "="*70)
        if all(self.results.values()):
            print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 PROJE TEZ SUNUMUNA HAZIR!{Colors.END}\n")
            return True
        else:
            print(f"\n{Colors.BOLD}{Colors.YELLOW}⚠️  EKSİKLER VAR, DÜZELTİLMELİ!{Colors.END}\n")
            print("Yukarıdaki uyarıları gözden geçirin ve düzeltin.")
            return False


def main():
    """Ana fonksiyon."""
    # Repository kök dizinini bul
    script_path = Path(__file__).resolve()
    repo_path = script_path.parent.parent
    
    print(f"\n{Colors.BOLD}Repository: {repo_path}{Colors.END}\n")
    
    # Checker'ı çalıştır
    checker = ThesisChecker(repo_path)
    success = checker.run_all_checks()
    
    # Çıkış kodu
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
