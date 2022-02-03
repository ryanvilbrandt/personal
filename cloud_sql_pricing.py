from enum import Enum


class Commitment(Enum):
    NONE = 1
    ONE_YEAR = 2
    THREE_YEAR = 3


CPU_PRICING = {Commitment.NONE: 30.15, Commitment.ONE_YEAR: 22.61, Commitment.THREE_YEAR: 14.47}
HA_CPU_PRICING = {Commitment.NONE: 60.30, Commitment.ONE_YEAR: 45.22, Commitment.THREE_YEAR: 28.94}
MEMORY_PRICING = {Commitment.NONE: 5.11, Commitment.ONE_YEAR: 3.83, Commitment.THREE_YEAR: 2.45}
HA_MEMORY_PRICING = {Commitment.NONE: 10.22, Commitment.ONE_YEAR: 7.67, Commitment.THREE_YEAR: 4.91}
STORAGE_PRICING = {"SSD": 0.170, "HDD": 0.090, "Backups": 0.080}
HA_STORAGE_PRICING = {"SSD": 0.340, "HDD": 0.180, "Backups": 0.080}


def pricing(cpus, memory, storage, storage_type, backups_enabled, high_availability, commitment):
    cpu_dict = HA_CPU_PRICING if high_availability else CPU_PRICING
    cpu_cost = cpu_dict[commitment] * cpus
    mem_dict = HA_MEMORY_PRICING if high_availability else MEMORY_PRICING
    mem_cost = mem_dict[commitment] * memory
    storage_dict = HA_STORAGE_PRICING if high_availability else STORAGE_PRICING
    storage_cost = storage_dict[storage_type] * storage
    backups_cost = storage_dict["Backups"] * storage if backups_enabled else 0

    print("{} vCPUs:    ${}/month".format(cpus, cpu_cost))
    print("{} GB memory: ${}/month".format(memory, mem_cost))
    print("{} GB {}: ${}/month".format(storage, storage_type, storage_cost))
    print("Backups enabled ({}): ${}/month".format(backups_enabled, backups_cost))
    print("High availability: {}".format(high_availability))
    print("Commitment: {}".format(commitment))
    print("")
    print("Total cost: ${}/month".format(cpu_cost + mem_cost + storage_cost + backups_cost))


pricing(32, 208, 30720, "HDD", True, True, Commitment.THREE_YEAR)
