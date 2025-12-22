#!/usr/bin/env python3

import struct
import binascii
import logging
import random
from typing import Dict, List, Tuple, Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants for A2S protocol
class A2SConstants:
    A2S_PREFIX = 0xFFFFFFFF  # This is -1 in two's complement
    A2S_QUERY_STR = b"Source Engine Query\0"
    A2S_INFO_REQUEST_HEADER = 0x54
    A2S_PLAYER_REQUEST_HEADER = 0x55
    A2S_RULES_REQUEST_HEADER = 0x56
    A2S_CHALLENGE_RESPONSE_HEADER = 0x41
    A2S_INFO_RESPONSE_HEADER = 0x49
    A2S_PLAYER_RESPONSE_HEADER = 0x44
    A2S_RULES_RESPONSE_HEADER = 0x45
    A2S_SERVERQUERY_GETCHALLENGE = 0x57  # Added for Master Server queries
    EDF_PORT = 0x80
    EDF_SOURCE_TV = 0x40
    EDF_STEAM_ID = 0x10
    EDF_KEYWORDS = 0x20
    EDF_GAME_ID = 0x01

class A2SServer:
    def __init__(self, server_config):
        self.config = server_config
        self.challenge = random.randint(-2147483648, 2147483647)
        
        # Initialize simulated players
        self.sim_players = []
        for i in range(min(len(self.config.get("player_names", [])), self.config.get("players_current", 1))):
            name = self.config.get("player_names", [])[i]
            score = random.randint(-50, 250)
            duration = random.uniform(0, 60)
            self.sim_players.append({"name": name, "score": score, "duration": duration})
            
        logger.info(f"A2S protocol handler initialized")
        #logger.info(f"A2S protocol handler initialized with challenge: 0x{self.challenge:x}")
    
    def update(self):
        """Update simulated player data and challenge periodically"""
        # Update player scores
        for player in self.sim_players:
            # Keep scores and durations more stable for better display
            if random.random() < 0.1:  # Only update 10% of the time
                player["score"] += random.randint(-1, 2)
            player["duration"] += 5
            
            # Make sure player info includes game mode
            if "game_mode" not in player and "game_mode" in self.config:
                player["game_mode"] = self.config["game_mode"]
        
        # Every ~5 minutes, update the challenge
        if random.random() < 0.003:  # ~0.3% chance per update (assuming ~1 update per second)
            self.update_challenge()
    
    def update_challenge(self):
        """Update challenge value"""
        self.challenge = random.randint(-2147483648, 2147483647)
        #logger.info(f"Updated challenge: 0x{self.challenge:x}")
    
    def decode_a2s_request(self, data: bytes) -> Optional[Tuple[int, int]]:
        """Decode A2S request packet"""
        if len(data) < 5:
            logger.warning(f"Received packet too short: {len(data)} bytes")
            return None
            
        try:
            #logger.debug(f"Decoding packet: {binascii.hexlify(data)}")
            
            # Check if the first 4 bytes are 0xFFFFFFFF (-1)
            if data[0:4] != b'\xff\xff\xff\xff':
                logger.warning(f"Invalid prefix: {binascii.hexlify(data[0:4])}")
                return None
            
            header = data[4]
            #logger.debug(f"Packet header: 0x{header:x}")
            
            # Handle Master Server challenge request
            if header == A2SConstants.A2S_SERVERQUERY_GETCHALLENGE:
                logger.debug("Master server query received")
                return (header, -1)
            
            if header == A2SConstants.A2S_INFO_REQUEST_HEADER:
                # Special case: if it's just the prefix and header and nothing else, respond immediately
                # This handles Steam's broadcast discovery
                if len(data) == 5:
                    #logger.debug("Received broadcast INFO request")
                    return (header, self.challenge)  # Use our own challenge
                
                # Verify query string
                if len(data) < 25:  # Minimum length for info request
                    logger.warning("INFO packet too short")
                    return None
                
                query_str = data[5:25]
                #logger.debug(f"Query string: {query_str}")
                
                if query_str != A2SConstants.A2S_QUERY_STR:
                    logger.warning(f"Invalid query string: {binascii.hexlify(query_str)}")
                    return None
                
                challenge = -1
                if len(data) > 25:
                    challenge_bytes = data[25:29]
                    challenge = struct.unpack("<i", challenge_bytes)[0]
                    #logger.debug(f"Received challenge: 0x{challenge:x}")
                
                return (header, challenge)
                
            elif header in (A2SConstants.A2S_PLAYER_REQUEST_HEADER, A2SConstants.A2S_RULES_REQUEST_HEADER):
                challenge = -1
                if len(data) >= 9:
                    challenge_bytes = data[5:9]
                    challenge = struct.unpack("<i", challenge_bytes)[0]
                    logger.debug(f"Received challenge: 0x{challenge:x}")
                
                return (header, challenge)
                
            logger.warning(f"Unrecognized packet header: 0x{header:x}")
            return None
        except Exception as e:
            logger.error(f"Error decoding request: {e}")
            return None
    
    def make_info_response_packet(self) -> bytes:
        """Create A2S_INFO response packet"""
        # Basic header
        packet = bytearray([0xFF, 0xFF, 0xFF, 0xFF, A2SConstants.A2S_INFO_RESPONSE_HEADER, self.config.get("protocol", 168)])
        
        # Server info strings
        packet.extend(self.config.get("name", "AoS Server").encode('ascii') + b'\0')
        packet.extend(self.config.get("map", "Unknown").encode('ascii') + b'\0')
        packet.extend(self.config.get("game_dir", "aceofspades").encode('ascii') + b'\0')
        packet.extend(self.config.get("game_name", "AoS").encode('ascii') + b'\0')
        
        # App ID
        packet.extend(struct.pack("<h", 0))
        
        # Player info
        current_players = self.config.get("players_current", len(self.sim_players))
        max_players = self.config.get("players_max", 20)
        packet.extend([
            current_players,
            max_players,
            self.config.get("num_bots", 0),
            self.config.get("server_type", b'd')[0],
            self.config.get("os", b'l')[0],
            self.config.get("password_protected", 0),
            self.config.get("secure", 1)
        ])

        # Version
        packet.extend(self.config.get("version", "1.0a1").encode('ascii') + b'\0')
        
        # Extra data flag
        edf = A2SConstants.EDF_PORT | A2SConstants.EDF_STEAM_ID | A2SConstants.EDF_KEYWORDS | A2SConstants.EDF_GAME_ID
        packet.extend([edf])
        
        # Extra data
        packet.extend(struct.pack("<H", self.config.get("game_port", 7777)))
        packet.extend(struct.pack("<q", self.config.get("steam_id", 224540)))

        
        # Format keywords to include mode in a standardized way
        keywords = self.config.get("keywords", "")
        packet.extend(keywords.encode('ascii') + b'\0')
        packet.extend(struct.pack("<q", self.config.get("app_id", 224540)))
        
        #logger.debug(f"Created INFO response packet: {len(packet)} bytes")
        return bytes(packet)
    
    def make_player_response_packet(self) -> bytes:
        """Create A2S_PLAYER response packet"""
        # Header
        packet = bytearray([0xFF, 0xFF, 0xFF, 0xFF, A2SConstants.A2S_PLAYER_RESPONSE_HEADER, len(self.sim_players)])
        
        # Player data
        for idx, player in enumerate(self.sim_players):
            packet.extend([idx])  # Index
            packet.extend(player["name"].encode('ascii') + b'\0')
            packet.extend(struct.pack("<i", int(player["score"])))
            packet.extend(struct.pack("<f", float(player["duration"])))
        
        #logger.debug(f"Created PLAYER response packet: {len(packet)} bytes")
        return bytes(packet)
    
    def make_rules_response_packet(self) -> bytes:
        """Create A2S_RULES response packet"""
        rules = self.config.get("rules", {})

        
        # Always ensure mode is in rules
        if "mode" not in rules and "game_mode" in self.config:
            rules["mode"] = self.config["game_mode"]
        
        # Header
        packet = bytearray([0xFF, 0xFF, 0xFF, 0xFF, A2SConstants.A2S_RULES_RESPONSE_HEADER])
        
        # Rule count
        packet.extend(struct.pack("<h", len(rules)))
        
        # Rules
        for key, value in rules.items():
            packet.extend(str(key).encode('ascii') + b'\0')
            packet.extend(str(value).encode('ascii') + b'\0')
        
        #logger.debug(f"Created RULES response packet: {len(packet)} bytes")
        return bytes(packet)
    
    def make_challenge_response_packet(self) -> bytes:
        """Create A2S_CHALLENGE response packet"""
        packet = bytearray([0xFF, 0xFF, 0xFF, 0xFF, A2SConstants.A2S_CHALLENGE_RESPONSE_HEADER])
        packet.extend(struct.pack("<i", self.challenge))
        #logger.debug(f"Created CHALLENGE response packet: {len(packet)} bytes")
        return bytes(packet)
    
    def handle_a2s_request(self, data: bytes):
        """Handle A2S request and return response"""
        result = self.decode_a2s_request(data)
        if not result:
            return None
            
        header, req_challenge = result
        
        # Handle broadcast discovery packets specially
        if len(data) == 5 and header == A2SConstants.A2S_INFO_REQUEST_HEADER:
            logger.info(f"Handling broadcast discovery")
            return self.make_info_response_packet()
            
        # Handle Master Server challenge request
        if header == A2SConstants.A2S_SERVERQUERY_GETCHALLENGE:
            logger.info(f"Sending challenge to master server")
            return self.make_challenge_response_packet()
            
        # Always respond to first-time queries with challenge, then to subsequent ones with data
        if req_challenge == -1 and header != A2SConstants.A2S_SERVERQUERY_GETCHALLENGE:
            #logger.info(f"New request, sending challenge response")
            return self.make_challenge_response_packet()
            
        if req_challenge != self.challenge and req_challenge != -1:
            logger.info(f"Challenge mismatch (got 0x{req_challenge:x}, expected 0x{self.challenge:x})")
            return self.make_challenge_response_packet()
            
        # Send appropriate response for valid challenge
        if header == A2SConstants.A2S_INFO_REQUEST_HEADER:
            logger.info(f"Sending INFO response")
            return self.make_info_response_packet()
        elif header == A2SConstants.A2S_PLAYER_REQUEST_HEADER:
            logger.info(f"Sending PLAYER response")
            return self.make_player_response_packet()
        elif header == A2SConstants.A2S_RULES_REQUEST_HEADER:
            logger.info(f"Sending RULES response")
            return self.make_rules_response_packet()
        else:
            logger.warning(f"Unknown header: 0x{header:x}")
            return None 