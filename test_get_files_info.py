from functions.get_files_info import get_files_info

def printgap(title):
    print("="*50)
    print(f"Result for {title} directory")

printgap("current")
print(get_files_info("calculator", "."))
printgap("pkg")
print(get_files_info("calculator", "pkg"))
printgap("/bin")
print(get_files_info("calculator", "/bin"))
printgap("../")
print(get_files_info("calculator", "../"))
