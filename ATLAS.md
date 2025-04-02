#include <iostream>
#include <pcap.h>
#include <vector>
#include <string>

void packetHandler(u_char *userData, const struct pcap_pkthdr *pkthdr, const u_char *packet) {
    std::cout << "Packet captured: " << pkthdr->len << " bytes" << std::endl;
}

std::string selectDevice() {
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_if_t *alldevs, *device;
    std::vector<std::string> deviceList;
    
    if (pcap_findalldevs(&alldevs, errbuf) == -1) {
        std::cerr << "Error finding devices: " << errbuf << std::endl;
        return "";
    }
    
    int i = 0;
    for (device = alldevs; device; device = device->next, ++i) {
        deviceList.push_back(device->name);
        std::cout << i + 1 << ": " << device->name << std::endl;
    }
    
    pcap_freealldevs(alldevs);
    
    if (deviceList.empty()) {
        std::cerr << "No devices found!" << std::endl;
        return "";
    }
    
    int choice;
    std::cout << "Select an interface (1-" << deviceList.size() << "): ";
    std::cin >> choice;
    
    if (choice < 1 || choice > deviceList.size()) {
        std::cerr << "Invalid choice!" << std::endl;
        return "";
    }
    
    return deviceList[choice - 1];
}

int main() {
    std::string deviceName = selectDevice();
    if (deviceName.empty()) return 1;
    
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_t *handle = pcap_open_live(deviceName.c_str(), BUFSIZ, 1, 1000, errbuf);
    if (!handle) {
        std::cerr << "Could not open device: " << errbuf << std::endl;
        return 1;
    }
    
    std::cout << "Listening on interface: " << deviceName << std::endl;
    
    pcap_loop(handle, 0, packetHandler, nullptr);
    
    pcap_close(handle);
    return 0;
}
