def solution(data, n):
    return [number for number in data if data.count(number) <= n]

if __name__ == "__main__":
    print(solution([1, 1, 2, 3, 4], 1))
