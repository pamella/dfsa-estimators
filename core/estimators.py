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


def simulate(
    estimator,
    initial_tag_amount,
    max_tag_amount,
    tag_increment_interval,
    max_repetition,
    initial_frame_size,
):
    list_tags_interval = []
    list_average_slots = []
    list_average_idles = []
    list_average_collisions = []
    list_average_success = []
    list_average_time = []

    for index in range(1, int(max_tag_amount / initial_tag_amount) + 1):
        # for index in range(int(max_tag_amount / initial_tag_amount)):
        tag_ammount = index * tag_increment_interval
        list_tags_interval.append(tag_ammount)

        average_slots = 0
        average_idles = 0
        average_collisions = 0
        average_success = 0
        average_time = 0

        for repetition in range(max_repetition):

            start_time = time.time()
            if estimator == 0:
                (
                    interaction_slots,
                    interaction_idles,
                    interaction_collisions,
                    interaction_success,
                ) = lower_bound(tag_ammount, initial_frame_size)
                average_slots += interaction_slots
                average_idles += interaction_idles
                average_collisions += interaction_collisions
                average_success += interaction_success
            if estimator == 1:
                eom_lee()
            end_time = time.time()
            interaction_time = end_time - start_time
            average_time += interaction_time

        list_average_slots.append(
            sum(list_average_slots) + (average_slots / max_repetition)
        )
        list_average_idles.append(
            sum(list_average_idles) + (average_idles / max_repetition)
        )
        list_average_collisions.append(
            sum(list_average_collisions) + (average_collisions / max_repetition)
        )
        list_average_success.append(
            sum(list_average_success) + (average_success / max_repetition)
        )
        list_average_time.append(
            sum(list_average_time) + (average_time / max_repetition)
        )

        print(
            list_tags_interval,
            list_average_slots,
            list_average_idles,
            list_average_collisions,
            list_average_success,
            list_average_time,
        )

    list_average_efficiency = [
        (list_average_success[i] / list_average_slots[i])
        for i in range(len(list_tags_interval))
    ]

    graph_plot(
        list_tags_interval,
        list_average_slots,
        "Número de Etiquetas",
        "Número de Slots Vazios",
        "lb_n_idle",
    )
    graph_plot(
        list_tags_interval,
        list_average_idles,
        "Número de Etiquetas",
        "Número de Slots",
        "lb_n_slots",
    )
    graph_plot(
        list_tags_interval,
        list_average_collisions,
        "Número de Etiquetas",
        "Número de Slots em Colisão",
        "lb_n_collisions",
    )
    graph_plot(
        list_tags_interval,
        list_average_efficiency,
        "Número de Etiquetas",
        "Eficiência (total de sucessos / total de slots)",
        "lb_n_efficiency",
    )
    graph_plot(
        list_tags_interval,
        list_average_time,
        "Número de Etiquetas",
        "Tempo para Identificação (s)",
        "lb_n_time",
    )

    return (
        list_average_slots,
        list_average_idles,
        list_average_collisions,
        list_average_time,
    )


def lower_bound(
    tag_ammount,
    frameSize,
):
    total_slots = 0
    total_idles = 0
    total_collisions = 0
    total_success = 0

    slots = [0] * frameSize
    while frameSize:
        total_slots += frameSize

        # Fulfill slots
        for _ in range(tag_ammount):
            random_slot = random.randrange(frameSize)
            slots[random_slot] += 1

        # Check for idles, sucess, and collisions
        local_success = 0
        local_collisions = 0
        for f in range(frameSize):
            if slots[f] == 0:
                total_idles += 1
            elif slots[f] == 1:
                local_success += 1
            elif slots[f] >= 2:
                local_collisions += 1

        tag_ammount -= local_success
        frameSize = int(local_collisions / 2)
        total_collisions += local_collisions
        total_success += local_success

    return total_slots, total_idles, total_collisions, total_success


def eom_lee():
    raise NotImplementedError("Eom-Lee has not been implemented.")
