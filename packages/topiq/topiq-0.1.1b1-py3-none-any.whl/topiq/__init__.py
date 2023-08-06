# Embedded topics

# Each Embedded topic can have multiple partitions; by using more partitions,
# the consumers of the messages (and the throughput) may be scaled and 
# concurrency of processing increased.

# On top of publish-subscribe with partitions, a point-to-point messaging 
# system is built, by putting a significant amount of logic into the 
# consumers (in the other messaging systems we’ve looked at, it was the 
# server that contained most of the message-consumed-by-one-consumer logic;
# here it’s the consumer).

# Each consumer in a consumer group reads messages from a number of dedicated
# partitions; hence it doesn’t make sense to have more consumer threads than 
# partitions. Messages aren’t acknowledged on server (which is a very 
# important design difference!), but instead message offsets processed by 
# consumers are written to Zookeeper, either automatically in the background,
# or manually.

from .version import get_version

VERSION = (0, 1, 1, 'beta', 1)

__version__ = get_version(VERSION)

from .consumer import *
from .message_type import *
from .message import *
from .partition import *
from .subscriber import *
from .topic_error import *
from .topic import *
