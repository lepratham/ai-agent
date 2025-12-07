from functions.get_files_info import get_files_info


result = get_files_info("calculator", ".")
print("Result for current directory:")
indented = "\n".join(f"  {line}" for line in result.split("\n") if line)
print(indented)

result = get_files_info("calculator", "pkg")
print("Result for 'pkg' directory:")
indented = "\n".join(f"  {line}" for line in result.split("\n") if line)
print(indented)

result = get_files_info("calculator", "/bin")
print("Result for '/bin' directory:")
indented = "\n".join(f"  {line}" for line in result.split("\n") if line)
print(indented)

result = get_files_info("calculator", "../")
print("Result for '../' directory:")
indented = "\n".join(f"  {line}" for line in result.split("\n") if line)
print(indented)
