"""
Custom MD5 implementation for length extension attack demonstrations.
Based on the MD5 specification (RFC 1321) with support for state manipulation.
"""

import struct

# MD5 auxiliary functions
F = lambda x, y, z: (x & y) | (~x & z)
G = lambda x, y, z: (x & z) | (y & ~z)
H = lambda x, y, z: x ^ y ^ z
I = lambda x, y, z: y ^ (x | ~z)

# MD5 constants (per-round sine-based values)
T = [int(abs(2**32 * __import__('math').sin(i + 1))) for i in range(64)]

def rotate_left(x, n):
    """Rotate x left by n bits (32-bit)."""
    return ((x << n) | (x >> (32 - n))) & 0xffffffff

def padding(msg_len_bits):
    """
    Generate MD5 padding for a message of given bit length.
    Returns the padding bytes that would be appended.
    """
    msg_len_bytes = msg_len_bits // 8
    # Padding: 0x80 followed by zeros, then 64-bit length
    pad_len = (55 - msg_len_bytes) % 64
    padding_bytes = b'\x80' + (b'\x00' * pad_len)
    # Append original length in bits as 64-bit little-endian
    padding_bytes += struct.pack('<Q', msg_len_bits)
    return padding_bytes

class md5:
    """MD5 hasher with support for state manipulation (for length extension attacks)."""
    
    def __init__(self, data=None, state=None, count=0):
        """
        Initialize MD5 hasher.
        
        Args:
            data: Initial data to hash (optional)
            state: Initial state as 16 bytes (optional, for length extension)
            count: Bit count of previously hashed data (for length extension)
        """
        if state is not None:
            # Initialize from existing state (for length extension attacks)
            if len(state) != 16:
                raise ValueError("State must be exactly 16 bytes")
            self.h = list(struct.unpack('<4I', state))
            self.count = count
            self.buf = b''
        else:
            # Standard initialization (MD5 magic numbers)
            self.h = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]
            self.count = 0
            self.buf = b''
        
        if data:
            self.update(data)
    
    def update(self, data):
        """Update the hash with new data."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        self.buf += data
        self.count += len(data) * 8
        
        # Process complete 64-byte blocks
        while len(self.buf) >= 64:
            self._process_block(self.buf[:64])
            self.buf = self.buf[64:]
    
    def _process_block(self, block):
        """Process a single 512-bit (64-byte) block."""
        # Break block into 16 32-bit words (little-endian)
        X = list(struct.unpack('<16I', block))
        
        # Initialize working variables
        A, B, C, D = self.h
        
        # Round 1
        for i in range(16):
            k = i
            s = [7, 12, 17, 22][i % 4]
            A = (B + rotate_left((A + F(B, C, D) + X[k] + T[i]) & 0xffffffff, s)) & 0xffffffff
            A, B, C, D = D, A, B, C
        
        # Round 2
        for i in range(16):
            k = (1 + 5 * i) % 16
            s = [5, 9, 14, 20][i % 4]
            A = (B + rotate_left((A + G(B, C, D) + X[k] + T[16 + i]) & 0xffffffff, s)) & 0xffffffff
            A, B, C, D = D, A, B, C
        
        # Round 3
        for i in range(16):
            k = (5 + 3 * i) % 16
            s = [4, 11, 16, 23][i % 4]
            A = (B + rotate_left((A + H(B, C, D) + X[k] + T[32 + i]) & 0xffffffff, s)) & 0xffffffff
            A, B, C, D = D, A, B, C
        
        # Round 4
        for i in range(16):
            k = (7 * i) % 16
            s = [6, 10, 15, 21][i % 4]
            A = (B + rotate_left((A + I(B, C, D) + X[k] + T[48 + i]) & 0xffffffff, s)) & 0xffffffff
            A, B, C, D = D, A, B, C
        
        # Add this block's hash to result so far
        self.h[0] = (self.h[0] + A) & 0xffffffff
        self.h[1] = (self.h[1] + B) & 0xffffffff
        self.h[2] = (self.h[2] + C) & 0xffffffff
        self.h[3] = (self.h[3] + D) & 0xffffffff
    
    def digest(self):
        """Return the digest as bytes."""
        # Make a copy to avoid modifying state
        h_copy = self.h[:]
        buf_copy = self.buf
        count_copy = self.count
        
        # Add padding
        padded = buf_copy + padding(count_copy)
        
        # Process final blocks
        temp = md5(state=struct.pack('<4I', *self.h), count=self.count - len(self.buf) * 8)
        temp.buf = b''
        for i in range(0, len(padded), 64):
            temp._process_block(padded[i:i+64])
        
        # Return digest as bytes
        return struct.pack('<4I', *temp.h)
    
    def hexdigest(self):
        """Return the digest as a hex string."""
        return self.digest().hex()


if __name__ == "__main__":
    # Test basic MD5
    h = md5()
    h.update(b"hello world")
    print("MD5('hello world') =", h.hexdigest())
    
    # Test padding function
    pad = padding(88)  # 11 bytes = 88 bits
    print(f"Padding for 88 bits: {pad.hex()}")
