import random
import time

from matplotlib import pyplot as plt


def graph_plot(x_values, y_values, x_label, y_label, file_name):
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.plot(x_values, y_values, linewidth=2)
    plt.grid()
    plt.savefig(f"graph_plots/{file_name}.png")
    plt.close()


def lower_bound(collisions):
    return collisions * 2


def eom_lee():
    raise NotImplementedError("Eom-Lee has not been implemented.")


def dfsa(estimator, current_tag, current_frame):
    total_slots = current_frame
    total_collisions = 0
    total_empty = 0

    start_time = time.time()
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
            current_frame = lower_bound(collisions)
        elif estimator == 1:
            current_frame = eom_lee()
        else:
            raise NotImplementedError()
        total_collisions += collisions
        total_slots += current_frame
        total_empty += empty

    end_time = time.time()
    total_time = end_time - start_time

    return total_collisions, total_slots, total_empty, total_time


def simulate(
    estimator,
    initial_tag_amount,
    max_tag_amount,
    tag_increment_interval,
    max_repetition,
    initial_frame_size,
):
    list_tags_interval = []
    list_avg_collisions = []
    list_avg_slots = []
    list_avg_empty = []
    list_avg_time = []

    for tag_index in range(1, int(max_tag_amount / initial_tag_amount) + 1):
        tags = tag_index * tag_increment_interval

        current_tag = tags
        current_frame = initial_frame_size

        avg_collisions = 0.0
        avg_slots = 0.0
        avg_empty = 0.0
        avg_time = 0.0

        current_repetition = max_repetition

        for i in range(current_repetition):
            current_tag = tags
            current_frame = initial_frame_size

            total_collisions, total_slots, total_empty, total_time = dfsa(
                estimator, current_tag, current_frame
            )

            avg_collisions += total_collisions
            avg_slots += total_slots
            avg_empty += total_empty
            avg_time += total_time

        avg_collisions /= current_repetition
        avg_slots /= current_repetition
        avg_empty /= current_repetition
        avg_time /= current_repetition

        list_avg_collisions.append(avg_collisions)
        list_avg_slots.append(avg_slots)
        list_avg_empty.append(avg_empty)
        list_avg_time.append(avg_time)

        list_tags_interval.append(tags)

        print(list_tags_interval, list_avg_collisions, list_avg_slots, list_avg_empty)

    graph_plot(
        list_tags_interval,
        list_avg_collisions,
        "Número de Etiquetas",
        "Número de Slots em Colisão",
        "lb_n_collisions",
    )
    graph_plot(
        list_tags_interval,
        list_avg_slots,
        "Número de Etiquetas",
        "Número de Slots Vazios",
        "lb_n_idle",
    )
    graph_plot(
        list_tags_interval,
        list_avg_empty,
        "Número de Etiquetas",
        "Número de Slots",
        "lb_n_slots",
    )
    graph_plot(
        list_tags_interval,
        list_avg_time,
        "Número de Etiquetas",
        "Tempo para Identificação (sec)",
        "lb_n_time",
    )
