// a1743596, Tang, Gordon
// 
// 
// team d

#include <iostream>
#include <fstream>
#include <deque>
#include <vector>

// std is a namespace: https://www.cplusplus.com/doc/oldtutorial/namespaces/
int TIME_ALLOWANCE = 8;  // allow to use up to this number of time slots at once
const int PRINT_LOG = 0; // print detailed execution trace

class Customer
{
public:
    std::string name;
    int priority;
    int arrival_time;
    int slots_remaining; // how many time slots are still needed
    int playing_since;
    int ageing;
    bool chance;

    Customer(std::string par_name, int par_priority, int par_arrival_time, int par_slots_remaining)
    {
        name = par_name;
        priority = par_priority;
        arrival_time = par_arrival_time;
        slots_remaining = par_slots_remaining;
        playing_since = -1;
        ageing = 0;
        chance = false;
    }
};

class Event
{
public:
    int event_time;
    int customer_id;  // each event involes exactly one customer

    Event(int par_event_time, int par_customer_id)
    {
        event_time = par_event_time;
        customer_id = par_customer_id;
    }
};

void initialize_system(
    std::ifstream &in_file,
    std::deque<Event> &arrival_events,
    std::vector<Customer> &customers)
{
    std::string name;
    int priority, arrival_time, slots_requested;

    // read input file line by line
    // https://stackoverflow.com/questions/7868936/read-file-line-by-line-using-ifstream-in-c
    int customer_id = 0;
    while (in_file >> name >> priority >> arrival_time >> slots_requested)
    {
        Customer customer_from_file(name, priority, arrival_time, slots_requested);
        customers.push_back(customer_from_file);

        // new customer arrival event
        Event arrival_event(arrival_time, customer_id);
        arrival_events.push_back(arrival_event);

        customer_id++;
    }
}

void print_state(
    std::ofstream &out_file,
    int current_time,
    int current_id,
    const std::deque<Event> &arrival_events,
    const std::deque<int> &customer_queue)
{
    out_file << current_time << " " << current_id << '\n';
    if (PRINT_LOG == 0)
    {
        return;
    }
    std::cout << current_time << ", " << current_id << '\n';
    for (int i = 0; i < arrival_events.size(); i++)
    {
        std::cout << "\t" << arrival_events[i].event_time << ", " << arrival_events[i].customer_id << ", ";
    }
    std::cout << '\n';
    for (int i = 0; i < customer_queue.size(); i++)
    {
        std::cout << "\t" << customer_queue[i] << ", ";
    }
    std::cout << '\n';
}

// process command line arguments
// https://www.geeksforgeeks.org/command-line-arguments-in-c-cpp/
int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        std::cerr << "Provide input and output file names." << std::endl;
        return -1;
    }
    std::ifstream in_file(argv[1]);
    std::ofstream out_file(argv[2]);
    if ((!in_file) || (!out_file))
    {
        std::cerr << "Cannot open one of the files." << std::endl;
        return -1;
    }

    // deque: https://www.geeksforgeeks.org/deque-cpp-stl/
    // vector: https://www.geeksforgeeks.org/vector-in-cpp-stl/
    std::deque<Event> arrival_events; // new customer arrivals
    std::vector<Customer> customers; // information about each customer

    // read information from file, initialize events queue
    initialize_system(in_file, arrival_events, customers);

    int current_id = -1; // who is using the machine now, -1 means nobody
    int time_out = -1; // time when current customer will be preempted
    int counter = 0;
    std::deque<int> queue; // waiting queue for priority 0
    std::deque<int> queue1; // waiting queue for priority 1

    // step by step simulation of each time slot
    bool all_done = false;
    for (int current_time = 0; !all_done; current_time++)
    {
        // welcome newly arrived customers
        while (!arrival_events.empty() && (current_time == arrival_events[0].event_time))
        {

            // add customers into different priority queues accordingly 
            if(customers[counter].priority == 0)
            {
                queue.push_back(arrival_events[0].customer_id);
            } else 
            {
                queue1.push_back(arrival_events[0].customer_id);
            }

            counter++;

            arrival_events.pop_front();
        }

        // check if we need to take a customer off the machine
        if (current_id >= 0)
        {
            if (current_time == time_out)
            {
                int last_run = current_time - customers[current_id].playing_since;
                customers[current_id].slots_remaining -= last_run;
                if (customers[current_id].slots_remaining > 0)
                {

                    // customer is not done yet, waiting for the next chance to play
                    if (customers[current_id].priority == 0)
                    {
                        queue.push_back(current_id);
                    } else if (customers[current_id].priority == 1)
                    {
                        queue1.push_back(current_id);
                    } else if(customers[current_id].priority == 0 && customers[current_id].chance == true )
                    {
                        // The customer will be sent to priority queue 1 if their chance is triggered
                        queue1.push_back(current_id);
                    }

                }
                current_id = -1; // the machine is free now
            }
        }

        // if machine is empty, schedule a new customer
        if (current_id == -1)
        {   
            int pos = 0;
            int temp = 0;
            int ageLimit = 18;
            if (!queue.empty()) // is anyone waiting in priority 0 queue?
            {

                // Find shortest remaining job first
                // If customers are not replaced when finding the smallest remaining playing time, the customer ages
                current_id = queue.front();
                for (int i = 0; i < queue.size(); i++)
                {
                    if (customers[queue.at(i)].slots_remaining < customers[current_id].slots_remaining)
                    {
                        current_id = queue.at(i);
                        pos = i;
                    } else {
                        customers[queue.at(i)].ageing++;
                    }
                }

                // Replace the srjf customer with the customer who has the highest age
                for (int i = 0; i < queue.size(); i++)
                {
                    if (customers[queue.at(i)].ageing > ageLimit)
                    {
                        if (customers[queue.at(i)].ageing > customers[current_id].ageing)
                        {
                            current_id = queue.at(i);
                            pos = i;
                        }
                    }
                }

                // If the customer's age is high, then allow it to play for small amount of time
                if (customers[current_id].ageing > ageLimit)
                {
                    TIME_ALLOWANCE = 6;
                } else {
                    TIME_ALLOWANCE = 8;
                }

                // Reset the customers age when they play game
                customers[current_id].ageing = 0;

                queue.erase(queue.begin() + pos);

                // Increase the customer's ages in priority queue 1
                // When the customer's age exceeds 20, it is queued in the priority 0 queue
                // And the customer's chance is triggered true
                // When the chance is triggered, the customer does not get another chance to play again in priority 0 queue
                if (!queue1.empty()){
                    for (int i = 0; i < queue1.size(); i++)
                    {
                        customers[queue1.at(i)].ageing++; 
                    }
                    if (customers[queue1.at(0)].ageing > ageLimit)
                    {
                        queue.push_front(queue1.front());
                        queue1.pop_front();
                        customers[queue1.at(0)].chance = true;
                    }  
                } 

                if (TIME_ALLOWANCE > customers[current_id].slots_remaining)
                {
                    time_out = current_time + customers[current_id].slots_remaining;
                }
                else
                {
                    time_out = current_time + TIME_ALLOWANCE;
                }
                customers[current_id].playing_since = current_time;

            } else if (!queue1.empty() && queue.empty()) // is anyone waiting in priority 1 queue?
            {
                
                // Find shortest remaining job first
                // If customers are not replaced when finding the smallest remaining playing time, the customer ages
                current_id = queue1.front();
                for (int i = 0; i < queue1.size(); i++)
                {
                    if (customers[queue1.at(i)].slots_remaining < customers[current_id].slots_remaining)
                    {
                        current_id = queue1.at(i);
                        pos = i;
                    } else {
                        customers[queue1.at(i)].ageing++;
                    }
                }

                // Replace the srjf customer with the customer who has the highest age
                for (int i = 0; i < queue1.size(); i++)
                {
                    if (customers[queue1.at(i)].ageing > ageLimit)
                    {
                        if (customers[queue1.at(i)].ageing > customers[current_id].ageing)
                        {
                            current_id = queue1.at(i);
                            pos = i;
                        }
                    }
                }

                // If the customer's age is high, then allow it to play for small amount of time
                if (customers[current_id].ageing > ageLimit)
                {
                    TIME_ALLOWANCE = 6;
                } else {
                    TIME_ALLOWANCE = 8;
                }

                customers[current_id].ageing = 0;

                queue1.erase(queue1.begin() + pos);

                if (TIME_ALLOWANCE > customers[current_id].slots_remaining)
                {
                    time_out = current_time + customers[current_id].slots_remaining;
                }
                else
                {
                    time_out = current_time + TIME_ALLOWANCE;
                }
                customers[current_id].playing_since = current_time;
            }
        }

        if (customers[counter].priority == 0)
        {
            print_state(out_file, current_time, current_id, arrival_events, queue);
        } else 
        {
            print_state(out_file, current_time, current_id, arrival_events, queue1);
        }

        // exit loop when there are no new arrivals, no waiting and no playing customers
        all_done = (arrival_events.empty() && queue1.empty() && queue.empty() && (current_id == -1));
    }

    return 0;
}
