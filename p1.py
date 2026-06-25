import subprocess
import os

class Command:
    def execute(self, content, filename):
        pass

class PythonExecuteCommand(Command):
    def execute(self, content, filename):
        temp_file = f"{filename}.py"
        with open(temp_file, "w") as f: f.write(content)
        result = subprocess.run(["python", temp_file], capture_output=True, text=True)
        os.remove(temp_file)
        return result.stdout or result.stderr

class JavaExecuteCommand(Command):
    def execute(self, content, filename):
        temp_file = "Main.java" 
        with open(temp_file, "w") as f: f.write(content)
        compile_res = subprocess.run(["javac", temp_file], capture_output=True, text=True)
        if compile_res.returncode == 0:
            run_res = subprocess.run(["java", "Main"], capture_output=True, text=True)
            return run_res.stdout
        return compile_res.stderr

class KotlinExecuteCommand(Command):
    def execute(self, content, filename):
        temp_file = f"{filename}.kt"
        temp_jar = f"{filename}.jar"
        
        with open(temp_file, "w") as f: 
            f.write(content)
            
        compile_res = subprocess.run(
            ["kotlinc", temp_file, "-include-runtime", "-d", temp_jar], 
            capture_output=True, text=True
        )
        
        if compile_res.returncode == 0:
            run_res = subprocess.run(["java", "-jar", temp_jar], capture_output=True, text=True)
            if os.path.exists(temp_file): os.remove(temp_file)
            if os.path.exists(temp_jar): os.remove(temp_jar)
            return run_res.stdout
        
        if os.path.exists(temp_file): os.remove(temp_file)
        return f"Eroare de compilare Kotlin:\n{compile_res.stderr}"



class BashExecuteCommand(Command):
    def execute(self, content, filename):
        temp_file = f"{filename}.bat"
        
        with open(temp_file, "w") as f:
            f.write(content)
        
        try:
            result = subprocess.run([temp_file], capture_output=True, text=True, shell=True)
            return result.stdout or result.stderr
        except Exception as e:
            return f"Eroare la execuția în CMD: {str(e)}"
        finally:
            if os.path.exists(temp_file):
                os.remove(temp_file)

# --- MODELUL CHAIN OF RESPONSIBILITY ---
class Handler:
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def handle(self, content, filename):
        if self.next_handler:
            return self.next_handler.handle(content, filename)
        return "Tip de fișier necunoscut."

class PythonHandler(Handler):
    def handle(self, content, filename):
        if "def " in content or "import sys" in content or "print(" in content:
            print(f"[Detector] Identificat ca: Python")
            return PythonExecuteCommand().execute(content, filename)
        return super().handle(content, filename)

class JavaHandler(Handler):
    def handle(self, content, filename):
        if "public class" in content or "System.out.print" in content:
            print(f"[Detector] Identificat ca: Java")
            return JavaExecuteCommand().execute(content, filename)
        return super().handle(content, filename)

class BashHandler(Handler):
    def handle(self, content, filename):
        if "echo " in content or "cd " in content:
            print(f"[Detector] Identificat ca: Bash")
            return BashExecuteCommand().execute(content, filename)
        return super().handle(content, filename)
    
class KotlinHandler(Handler):
    def handle(self, content, filename):
        keywords = ["fun main", "println(", "val ", "var ", "fun ", "data class"]
        if any(key in content for key in keywords):
            print(f"[Detector] Identificat ca: Kotlin")
            return KotlinExecuteCommand().execute(content, filename)
        return super().handle(content, filename)

def main():
    file_path = input("Introduceti numele fisierului: ")
    
    if not os.path.exists(file_path):
        print("Fisierul nu exista.")
        return

    with open(file_path, "r") as f:
        continut = f.read()

    chain = PythonHandler(JavaHandler(KotlinHandler(BashHandler())))

    output = chain.handle(continut, file_path)
    
    print("\n--- REZULTAT EXECUȚIE ---")
    print(output)

if __name__ == "__main__":
    main()