import math
import random
import time

from matplotlib import pyplot as plt


def lower_bound(collisions):
    return collisions * 2


def eom_lee(collisions, success, frame_size):
    EPS = 1e-3
    gama0 = 0.0
    gama1 = 2.0
    beta = 0.0
    exp = 0.0

    while True:
        gama0 = gama1
        beta = frame_size / (gama0 * collisions + success)
        exp = math.exp(-1.0 / beta)
        gama1 = (1.0 - exp) / (beta * (1.0 - ((1.0 + (1.0 / beta)) * exp)))

        if not abs(gama0 - gama1) >= EPS:
            break

    return int(gama1 * collisions)


def dfsa(estimator, current_tag, current_frame):
    total_slots = current_frame
    total_collisions = 0
    total_empty = 0
    total_success = 0
    total_time = 0

    while current_tag > 0:
        frame = [0] * current_frame

        success = 0
        collisions = 0
        empty = 0

        for i in range(current_tag):
            random_index = random.randrange(current_frame)
            frame[random_index] += 1

        for i in range(current_frame):
            if frame[i] == 0:
                empty += 1
            elif frame[i] == 1:
                success += 1
            elif frame[i] >= 2:
                collisions += 1

        current_tag -= success

        if estimator == 0:
            start_time = time.time()
            current_frame = lower_bound(collisions)
            total_time += time.time() - start_time
        elif estimator == 1:
            start_time = time.time()
            current_frame = eom_lee(collisions, success, current_frame)
            total_time += time.time() - start_time
        else:
            raise NotImplementedError()

        total_collisions += collisions
        total_slots += current_frame
        total_empty += empty
        total_success += success

    return total_collisions, total_slots, total_empty, total_success, total_time


def simulate(
    estimators,
    initial_tag_amount,
    max_tag_amount,
    tag_increment_interval,
    max_repetition,
    initial_frame_size,
):
    estimator_results = {}

    for estimator in range(1 if estimators == 0 else estimators):
        if estimators == 1:
            estimator = 1
        if estimators == 0:
            estimator = 0

        list_tags_interval = []
        list_avg_collisions = []
        list_avg_slots = []
        list_avg_empty = []
        list_avg_time = []
        list_avg_efficiency = []
        for tag_index in range(1, int(max_tag_amount / initial_tag_amount) + 1):
            tags = tag_index * tag_increment_interval

            current_tag = tags
            current_frame = initial_frame_size

            avg_collisions = 0.0
            avg_slots = 0.0
            avg_empty = 0.0
            avg_success = 0.0
            avg_time = 0.0

            current_repetition = max_repetition

            for i in range(current_repetition):
                current_tag = tags
                current_frame = initial_frame_size

                (
                    total_collisions,
                    total_slots,
                    total_empty,
                    total_success,
                    total_time,
                ) = dfsa(estimator, current_tag, current_frame)

                avg_collisions += total_collisions
                avg_slots += total_slots
                avg_empty += total_empty
                avg_success += total_success
                avg_time += total_time

            avg_collisions /= current_repetition
            avg_slots /= current_repetition
            avg_empty /= current_repetition
            avg_success /= current_repetition
            avg_time /= current_repetition

            list_avg_collisions.append(avg_collisions)
            list_avg_slots.append(avg_slots)
            list_avg_empty.append(avg_empty)
            list_avg_time.append(avg_time)
            list_avg_efficiency.append(avg_success / avg_slots)

            list_tags_interval.append(tags)

            print(
                list_tags_interval,
                list_avg_collisions,
                list_avg_slots,
                list_avg_efficiency,
                list_avg_empty,
            )
        graph_plot_file_name_prefix = ""
        if estimator == 0:
            graph_plot_file_name_prefix = "lower_bound"
        if estimator == 1:
            graph_plot_file_name_prefix = "eom_lee"
        if estimators == 2:
            graph_plot_file_name_prefix = "lower_boundxeom_lee"
        estimator_results[estimator] = {
            "graph_plot_file_name_prefix": graph_plot_file_name_prefix,
            "list_tags_interval": list_tags_interval,
            "list_avg_collisions": list_avg_collisions,
            "list_avg_slots": list_avg_slots,
            "list_avg_empty": list_avg_empty,
            "list_avg_efficiency": list_avg_efficiency,
            "list_avg_time": list_avg_time,
        }

        simulation_plot_graphs(estimator_results)


def simulation_plot_graphs(estimator_results):
    colors = ["blue", "green"]
    labels = ["Lower Bound", "Eom-Lee"]
    markers = ["x", "s"]
    for result in estimator_results:
        plt.xlabel("N??mero de Etiquetas")
        plt.ylabel("N??mero de Slots em Colis??o")
        plt.plot(
            estimator_results[result]["list_tags_interval"],
            estimator_results[result]["list_avg_collisions"],
            linewidth=2,
            color=colors[result],
            label=labels[result],
            marker=markers[result],
        )
        plt.xticks(
            estimator_results[result]["list_tags_interval"],
            estimator_results[result]["list_tags_interval"],
        )
        plt.yticks([i * 200 for i in range(10)], [i * 200 for i in range(10)])
        plt.legend()
        plt.grid(True)
        plt.savefig(
            f"graph_plots/{estimator_results[result]['graph_plot_file_name_prefix']}_n_collisions.png"
        )
    plt.close()

    for result in estimator_results:
        plt.xlabel("N??mero de Etiquetas")
        plt.ylabel("N??mero de Slots")
        plt.plot(
            estimator_results[result]["list_tags_interval"],
            estimator_results[result]["list_avg_slots"],
            linewidth=2,
            color=colors[result],
            label=labels[result],
            marker=markers[result],
        )
        plt.xticks(
            estimator_results[result]["list_tags_interval"],
            estimator_results[result]["list_tags_interval"],
        )
        plt.yticks([i * 500 for i in range(8)], [i * 500 for i in range(8)])
        plt.legend()
        plt.grid(True)
        plt.savefig(
            f"graph_plots/{estimator_results[result]['graph_plot_file_name_prefix']}_n_slots.png"
        )
    plt.close()

    for result in estimator_results:
        plt.xlabel("N??mero de Etiquetas")
        plt.ylabel("N??mero de Slots Vazios")
        plt.plot(
            estimator_results[result]["list_tags_interval"],
            estimator_results[result]["list_avg_empty"],
            linewidth=2,
            color=colors[result],
            label=labels[result],
            marker=markers[result],
        )
        plt.xticks(
            estimator_results[result]["list_tags_interval"],
            estimator_results[result]["list_tags_interval"],
        )
        plt.yticks([i * 100 for i in range(12)], [i * 100 for i in range(12)])
        plt.legend()
        plt.grid(True)
        plt.savefig(
            f"graph_plots/{estimator_results[result]['graph_plot_file_name_prefix']}_n_empty.png"
        )
    plt.close()

    for result in estimator_results:
        plt.xlabel("N??mero de Etiquetas")
        plt.ylabel("Efici??ncia (total sucessos / total slots)")
        plt.plot(
            estimator_results[result]["list_tags_interval"],
            estimator_results[result]["list_avg_efficiency"],
            linewidth=2,
            color=colors[result],
            label=labels[result],
            marker=markers[result],
        )
        plt.xticks(
            estimator_results[result]["list_tags_interval"],
            estimator_results[result]["list_tags_interval"],
        )
        plt.legend()
        plt.grid(True)
        plt.savefig(
            f"graph_plots/{estimator_results[result]['graph_plot_file_name_prefix']}_n_efficiency.png"
        )
    plt.close()

    for result in estimator_results:
        plt.xlabel("N??mero de Etiquetas")
        plt.ylabel("Tempo para Identifica????o (s)")
        plt.plot(
            estimator_results[result]["list_tags_interval"],
            estimator_results[result]["list_avg_time"],
            linewidth=2,
            color=colors[result],
            label=labels[result],
            marker=markers[result],
        )
        plt.xticks(
            estimator_results[result]["list_tags_interval"],
            estimator_results[result]["list_tags_interval"],
        )
        plt.legend()
        plt.grid(True)
        plt.savefig(
            f"graph_plots/{estimator_results[result]['graph_plot_file_name_prefix']}_n_time.png"
        )
    plt.close()
