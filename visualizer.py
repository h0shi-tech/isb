import matplotlib.pyplot as plt
import multiprocessing as mp
from collision_finder import find_collision

def measure_time_and_plot():
    """
    Измеряет время выполнения для разного количества процессов и строит график результатов.
    
    Возвращает:
        tuple: (найденный номер карты, список количества процессов, список времени выполнения)
    """
    max_processes = int(mp.cpu_count() * 1.5)
    processes_list = list(range(1, max_processes + 1))
    times = []
    found_card = None
    
    for processes in processes_list:
        time_taken, result = find_collision(processes)
        times.append(time_taken)
        if result and not found_card:
            found_card = result
            
    return found_card, processes_list, times

def visualize_results(processes_list, times):
    """
    Создает и сохраняет график времени выполнения в зависимости от количества процессов.
    
    Аргументы:
        processes_list (list): Список количества процессов
        times (list): Список времени выполнения
    """
    plt.figure(figsize=(10, 6))
    plt.plot(processes_list, times, 'b-', label='Execution Time')
    plt.scatter(processes_list, times, color='blue')
    
    # Найти и отметить минимальную точку
    min_time_idx = times.index(min(times))
    plt.scatter(processes_list[min_time_idx], times[min_time_idx], 
                color='red', s=100, label='Minimum Time')
    
    plt.xlabel('Number of Processes')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Hash Collision Search Performance')
    plt.grid(True)
    plt.legend()
    
    # Сохранить график
    plt.savefig('performance_plot.png')
    plt.close() 