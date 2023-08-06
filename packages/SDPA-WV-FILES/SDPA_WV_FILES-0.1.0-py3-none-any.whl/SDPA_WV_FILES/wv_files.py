from struct import unpack, pack
from datetime import datetime
from enum import Enum
import numpy as np

LENGTH_SPECIFIED_TAGS = [b"EMPTYTAG", b"WAVEFORM"]


class Tags(Enum):
    WAVEFORM_TAG = b'WAVEFORM'
    EMPTYTAG_TAG = b'EMPTYTAG'
    CLOCK_TAG = b'CLOCK'
    COMMENT_TAG = b'COMMENT'
    COPYRIGHT_TAG = b'COPYRIGHT'
    DATE_TAG = b'DATE'
    SAMPLES_TAG = b'SAMPLES'
    LEVEL_OFFSET_TAG = b'LEVEL OFFS'
    TYPE_TAG = b'TYPE'

DATETIME_FORMAT = '%Y-%m-%d;%H:%M:%S'


def _content_to_dict(data):
    """
    Returns a dictionnary with the content of data

    Parameters
    ----------
    data : bytearray
        Raw data of file

    Returns
    -------
    contents : dict
        Contents of the file organised by tags
    """
    contents = {}
    p = 0
    while(p >= 0):
        # Process the current tag (starting at p+1)
        tag = data[p+1:].split(b':', 1)[0]
        length_specified = False
        for l in [Tags.WAVEFORM_TAG.value, Tags.EMPTYTAG_TAG.value]:
            if l in tag:
                # This is a length-specified tag (with -xxx)
                length_specified = True
                tag, length_ba = tag.split(b'-')
                length = int(length_ba)
                # +1 to remove the #
                value_start = p + 1 + \
                    len(tag) + len(b'-') + len(length_ba) + len(b':') + 1
                # -1 to remove the } at the end
                value_end = value_start + length - 1
                break
        else:
            # Not a length specified tag
            value_start = p + 1 + len(tag) + len(b':')
            value_end = value_start + data[value_start:].find(b'}')

        value = data[value_start:value_end]

        #print(f"{tag} -> {value}")
        contents[tag] = value

        p = data.find(b'{', value_end+1)
    return contents


def _bytearray_to_waveform(data):
    """
    Parses a .wv file content and stores the I and Q values

    Parameters
    ----------
    data : bytearray
        Raw data contained in the .wv file

    Returns
    -------
    I : array_like
        I values
    Q : array_like
        Q values
    """
    def pairwise(iterable):
        "s -> (s0, s1), (s2, s3), (s4, s5), ..."
        a = iter(iterable)
        return zip(a, a)

    values = []
    for w in pairwise(data):
        ba = bytearray(w)
        value = unpack('<h', ba)[0]
        values.append(value)

    # Normalise -32768..32767 -> -1..1
    I = np.array(values[::2]) / 2**(16-1)
    Q = np.array(values[1::2]) / 2**(16-1)

    return I, Q


def _waveform_to_bytearray(I, Q):
    """
    Return a .wv file compatible bytearray from I and Q values

    Parameters
    ----------
    I : list or array_like
        list of I values
    Q : list or array_liek
        list of Q values

    Returns
    -------
    data : bytearray
        waveform data in bytearray format
    """

    if len(I) != len(Q):
        raise ValueError("I and Q must be the same size")

    ba = b''
    for i, q in zip(I, Q):
        i_ba = pack('<h', int(np.round(i*(2**(16-1)-1))))  # Formats as signed 16-bit
        q_ba = pack('<h', int(np.round(q*(2**(16-1)-1))))
        ba += i_ba
        ba += q_ba

    return ba


def _dict_to_contents(dict):
    """
    Prepares .wv file contents with the given tags and values

    Parameters
    ----------
    dict : dict
        Dictionnary containing the tags and values. Everything must be bytearray including the keys
    
    Returns
    -------
    data : bytearray
        Data of the .wv file
    """
    WAVEFORM_KEY = b'WAVEFORM'
    EMPTYTAG_KEY = b'EMPTYTAG'
    if not WAVEFORM_KEY in dict.keys():
        raise ValueError(f"Missing {WAVEFORM_KEY} in dictionnary keys")
    
    data = b''
    # Adding the first tags
    for key, value in dict.items():
        if key not in [WAVEFORM_KEY, EMPTYTAG_KEY]:
            data += b'{' + key + b':' + value + b'}'

    # Add the padding (empty tag)
    # The waveform must start at 0x4000
    padding_length = 0x4000 - len(data)
    # Force 5 bytes for the length, otherwise we could have big problems when it's 999-1000 for example
    empty_tag_length = padding_length - 10 - len(EMPTYTAG_KEY)
    empty_tag = b'{' + EMPTYTAG_KEY + b'-' + f'{empty_tag_length+1:05d}'.encode(
        'ASCII') + b':#' + b'\x20'*empty_tag_length + b'}'

    # Add the waveform data
    waveform_data = b'{' + WAVEFORM_KEY + b'-' + \
        str(len(value) + 1).encode('ascii') + \
        b':#' + dict[WAVEFORM_KEY] + b'}'
    data += empty_tag + waveform_data

    return data


class Waveform_file():
    def __init__(self):
        """
        Instance of a waveform file (.wv)
        """
        self.copyright = None
        self.comment = None
        self.I = None
        self.Q = None

    def write(self, filename):
        """
        Writes a .wv file with the given waveform (I and Q)

        Parameters
        ----------
        filename : str
            File path (with extension)
        """
        # See SMBV100B user manual 4.6.5.1
        # As per example given by SMCV100B we must (could) include :
        # - Type (mandatory, must be the first tag in the file)
        #   - SMU-WV : valid SMBV100B waveform
        #   - SMU-MWV : valid SMBV100B multi-segment waveform
        #   - SMU-DL : valid WMBV100B data list
        #   - SMU-CL : valid WMBV100B control list
        # - checksum (right after type)
        # - Copyright
        # - Date
        # - Clock
        # - Samples
        # - Level offset
        # - Comment
        # - Emptytag
        # - waveform
        type = b"SMU-WV"

        def checksum(data):
            def quarterwise(iterable):
                "s -> (s0, s1, s2, s3), (s4, s5, s6, s7), ..."
                a = iter(iterable)
                return zip(a, a, a, a)

            result = 0xA50F74FF
            for d in quarterwise(data):
                ba = bytearray(d)
                value = unpack('<L', ba)[0]
                result = result ^ value
            return result

        _dict = {}
        # Encode the data
        waveform_data = _waveform_to_bytearray(self.I, self.Q)
        # Make the checksum
        checksum_ba = str(checksum(waveform_data)).encode('ASCII')
        checksum_ba_pad = b'\x20' * (20-len(checksum_ba)) + checksum_ba

        # Write type + checksum
        _dict[Tags.TYPE_TAG.value] = type + b',' + checksum_ba_pad

        if self.copyright is not None:
            # Write copyright
            _dict[Tags.COPYRIGHT_TAG.value] = self.copyright.encode('ASCII')

        # Write date
        now = datetime.now()
        _dict[Tags.DATE_TAG.value] = now.strftime(DATETIME_FORMAT).encode('ASCII')

        # Write clock (in Hz)
        _dict[Tags.CLOCK_TAG.value] = f"{self.clock:.0f}".encode('ASCII')

        # Write samples
        samples = len(self.I)
        _dict[Tags.SAMPLES_TAG.value] = str(samples).encode('ASCII')

        # Write level offset
        _dict[Tags.LEVEL_OFFSET_TAG.value] = b'0.0,0.0'  # maybe change this

        if self.comment is not None:
            # Write comment
            _dict[Tags.COMMENT_TAG.value] = self.comment.encode('ASCII')

        # The empty tag is managed by the write procedure

        # Write the data
        _dict[b'WAVEFORM'] = waveform_data

        print(f"samples : {samples}")

        with open(filename, 'wb') as f:
            data = _dict_to_contents(_dict)
            f.write(data)

    def read(self, filename):
        """
        Opens the .wv file

        Parameters
        ----------
        filename : str
            File path (with extension)
        """
        # parse a file and creates a dictionnary containing the tags and corresponding values
        # Everything (keys and values) is bytearray
        _dict = {}
        with open(filename, 'rb') as f:
            data = f.read()
            _dict = _content_to_dict(data)

            self.clock = float(_dict[Tags.CLOCK_TAG.value])
            self.comment = _dict[Tags.COMMENT_TAG.value].decode()
            self.copyright = _dict[Tags.COPYRIGHT_TAG.value].decode()
            self.I, self.Q = _bytearray_to_waveform(_dict[Tags.WAVEFORM_TAG.value])
            self.date = datetime.strptime(_dict[Tags.DATE_TAG.value].decode(), DATETIME_FORMAT)
            
