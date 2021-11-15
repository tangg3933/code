#include <iostream>
#include <fstream>
#include <deque>
#include <vector>
#include <stdlib.h>
#include <time.h>

void print_state(std::ofstream &out_file, std::string current_id, int priority, int entry_time, int play_time)
{
    out_file << current_id << " " << priority << " " << entry_time << " " << play_time << '\n';
}

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        std::cerr << "Provide output file name." << std::endl;
        return -1;
    }
    std::ofstream out_file(argv[1]);
    if (!out_file)
    {
        std::cerr << "Cannot open the output file." << std::endl;
        return -1;
    }

    const int customer_count = 50;

    srand(time(NULL));
    //first customer enter between 0-10
    int first_entry = rand() % 11;
    int last_entry = first_entry;
    int entry = first_entry;
    int next_entry_range = 9;

    for (int customer = 0; customer < customer_count; customer++)
    {
        entry = rand() % next_entry_range + last_entry; 
        last_entry = entry;
        std::string customer_id = customer < 10 ? "c0"+std::to_string(customer) : "c"+std::to_string(customer);
        print_state(out_file, customer_id, rand() % 2, entry, rand() % 100 + 1);
    }

    return 0;
}
