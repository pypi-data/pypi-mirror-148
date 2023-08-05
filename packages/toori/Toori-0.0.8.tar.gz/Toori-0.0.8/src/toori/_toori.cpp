#include <iostream>
#include <WinSock2.h>
#include <WS2tcpip.h>
#include <Windows.h>
#include <pybind11/pybind11.h>
#include <windivert.h>
#include <stdio.h>
#include <exception>

#define ntohs(x) WinDivertHelperNtohs(x)
#define ntohl(x) WinDivertHelperNtohl(x)
#define htons(x) WinDivertHelperHtons(x)
#define htonl(x) WinDivertHelperHtonl(x)

#define MAXBUF WINDIVERT_MTU_MAX

std::string CLIENT_IP = "";

namespace py = pybind11;

HANDLE hOutbound = INVALID_HANDLE_VALUE;
HANDLE hInbound = INVALID_HANDLE_VALUE;

bool showHashesFlag = false;

// Generic TooriException class
class TooriException : public std::exception {
public:
	explicit TooriException(const char* m) : message{ m } {}
	const char* what() const noexcept override { return message.c_str(); }

private:
	std::string message = "";
};

// WinDivert Exception class to translate error codes from GetLastError()
class WinDivertException : public std::exception {
public:
	//explicit WinDivertException(DWORD m) : errCode{ m } {}
	const char* what() const noexcept override {
		switch (GetLastError()) {
		case 2:
			return "ERROR_FILE_NOT_FOUND";
		case 5:
			return "ERROR_ACCESS_DENIED";
		case 87:
			return "ERROR_INVALID_PARAMETER";
		case 122:
			return "ERROR_INSUFFICIENT_BUFFER";
		case 232:
			return "ERROR_NO_DATA";
		case 577:
			return "ERROR_INVALID_IMAGE_HASH";
		case 654:
			return "ERROR_DRIVER_FAILED_PRIOR_UNLOAD";
		case 1060:
			return "ERROR_SERVICE_DOES_NOT_EXIST";
		case 1275:
			return "ERROR_DRIVER_BLOCKED";
		case 1753:
			return "EPT_S_NOT_REGISTERED";
		default:
			return "Unrecognized WinDivert Error";
		}
	}
};

void showHashes() {
	showHashesFlag = true;
}

// Initialize outbound listener
void initOutbound(char* outboundFilter) {
	if (hOutbound != INVALID_HANDLE_VALUE)
		throw TooriException("Reinitialization of Outbound Listener");

	hOutbound = WinDivertOpen(outboundFilter, WINDIVERT_LAYER_NETWORK, WINDIVERT_PRIORITY_HIGHEST, WINDIVERT_FLAG_RECV_ONLY);
	if (hOutbound == INVALID_HANDLE_VALUE)
		throw WinDivertException();
}

// Open for sending (injecting) only
void initInbound(std::string cli_ip) {
	if (hInbound != INVALID_HANDLE_VALUE)
		throw TooriException("Reinitialization of Inbound Listener");

	hInbound = WinDivertOpen("false", WINDIVERT_LAYER_NETWORK, 0, WINDIVERT_FLAG_SEND_ONLY);
	if (hInbound == INVALID_HANDLE_VALUE)
		throw WinDivertException();

	CLIENT_IP = cli_ip;
}


// Receive one outbound packet and return it as a std::string
std::string recvOnce() {
	py::gil_scoped_release release;
	if (hOutbound == INVALID_HANDLE_VALUE)
		throw TooriException("Outbound Listener Uninitialized");

	WINDIVERT_ADDRESS addrOutbound;
	UINT8 packetOutbound[MAXBUF];
	UINT packetOutboundLen;

	// Intercept packets based on WinDivertOpen filter
	if (!WinDivertRecv(hOutbound, packetOutbound, sizeof(packetOutbound), &packetOutboundLen, &addrOutbound))
	{
		//std::cerr << "WinDivertRecv failed to read packet " << GetLastError() << std::endl;
		throw WinDivertException();
		// Skip packet on error?
	}
	if (showHashesFlag)
	{
		UINT64 packetOutboundHash = WinDivertHelperHashPacket(packetOutbound, packetOutboundLen, 0);
		std::cout << packetOutboundHash << std::endl;
	}

	py::gil_scoped_acquire acquire;
	return std::string((char*)packetOutbound, packetOutboundLen);
}

void injectOnce(std::string pi) {
	if (hInbound == INVALID_HANDLE_VALUE)
		throw TooriException("Inbound Listener Uninitialized");

	PVOID packetInbound = (PVOID)pi.c_str();
	UINT packetInboundLen = (UINT)pi.length();
	WINDIVERT_ADDRESS addrInbound;
	UINT64 packetInboundHash = 0;
	PWINDIVERT_IPHDR ipHeaderInbound;
	PWINDIVERT_TCPHDR tcpHeaderInbound;
	PWINDIVERT_UDPHDR udpHeaderInbound;
	char srcBufInbound[INET6_ADDRSTRLEN + 1];
	char dstBufInbound[INET6_ADDRSTRLEN + 1];
	UINT32 clientIpBuf[4];

	if (!WinDivertHelperParsePacket(packetInbound, packetInboundLen, &ipHeaderInbound, NULL, NULL, NULL, NULL, &tcpHeaderInbound, &udpHeaderInbound, NULL, NULL, NULL, NULL))
	{
		std::cerr << "WinDivertHelperParsePacket failed" << std::endl;
		return;
	}

	addrInbound.Outbound = 1;

	if (!WinDivertHelperFormatIPv4Address(ntohl(ipHeaderInbound->SrcAddr), srcBufInbound,
		sizeof(srcBufInbound)))
	{
		std::cerr << "WinDivertHelperFormatIPv4Address SrcAddr failed" << std::endl;
		return;
	}

	if (!WinDivertHelperFormatIPv4Address(ntohl(ipHeaderInbound->DstAddr), dstBufInbound,
		sizeof(dstBufInbound)))
	{
		std::cerr << "WinDivertHelperFormatIPv4Address DstAddr failed" << std::endl;
		return;
	}

	
	if (showHashesFlag)
	{
		UINT64 packetInboundHash = WinDivertHelperHashPacket(packetInbound, packetInboundLen, 0);
		std::cout << packetInboundHash << std::endl;

		// printf("INBOUND PACKET \n"
		// "Size: %u bytes\n"
		// "Src: %s\n"
		// "Dst: %s\n"
		// "Dst (new): %s\n",
		// packetInboundLen,
		// srcBufInbound,
		// dstBufInbound,
		// CLIENT_IP);

		// printf("TCP Header: SrcPort=%u DstPort=%u SeqNum=%u AckNum=%u "
		// "HdrLength=%u Reserved1=%u Reserved2=%u Urg=%u Ack=%u "
		// "Psh=%u Rst=%u Syn=%u Fin=%u Window=%u Checksum=0x%.4X "
		// "UrgPtr=%u\n",
		// ntohs(tcpHeaderInbound->SrcPort), ntohs(tcpHeaderInbound->DstPort),
		// ntohl(tcpHeaderInbound->SeqNum), ntohl(tcpHeaderInbound->AckNum),
		// tcpHeaderInbound->HdrLength, tcpHeaderInbound->Reserved1,
		// tcpHeaderInbound->Reserved2, tcpHeaderInbound->Urg, tcpHeaderInbound->Ack,
		// tcpHeaderInbound->Psh, tcpHeaderInbound->Rst, tcpHeaderInbound->Syn,
		// tcpHeaderInbound->Fin, ntohs(tcpHeaderInbound->Window),
		// ntohs(tcpHeaderInbound->Checksum), ntohs(tcpHeaderInbound->UrgPtr));
	}

	if (!WinDivertHelperParseIPv4Address(CLIENT_IP.c_str(), clientIpBuf))
	{
		std::cerr << "WinDivertHelperParseIPv4Address failed" << std::endl;
		return;
	}

	ipHeaderInbound->DstAddr = htonl(*clientIpBuf);

	if (!WinDivertHelperCalcChecksums((PVOID)packetInbound, packetInboundLen, &addrInbound, 0))
	{
		std::cerr << "WinDivertHelperCalcChecksums failed" << std::endl;
		return;
	}

	if (!WinDivertSend(hInbound, (PVOID)packetInbound, packetInboundLen, NULL, &addrInbound))
		throw WinDivertException();
}

PYBIND11_MODULE(_toori, m) {
	auto tooriException = py::register_exception<TooriException>(m, "TooriException");
	auto winDivertException = py::register_exception<WinDivertException>(m, "WinDivertException");

	m.def("recv_once",
		[]() {
			return py::bytes(recvOnce());  // Return the data without transcoding
		}, R"pbdoc(
		Receive one outbound packet.
	)pbdoc");

	m.def("init_outbound", &initOutbound, R"pbdoc(
		Initialise outbound sniffer.
	)pbdoc",
	py::arg("filter"));

	m.def("show_hashes", &showHashes, R"pbdoc(
        Show packet hashes.
    )pbdoc");

	m.def("init_inbound", &initInbound, R"pbdoc(
        Initialise inbound injector.
    )pbdoc",
	py::arg("client_ip"));

	m.def("inject_once", &injectOnce, R"pbdoc(
		Inject one outbound packet.
    )pbdoc");
}
