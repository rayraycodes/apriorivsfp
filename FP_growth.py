from collections import defaultdict, namedtuple

class Node(namedtuple('Node', 'value, count, parent, children')):
    def increment(self):
        return self._replace(count=self.count + 1)

def FP_Growth(transactions, minimum_support):
    items = defaultdict(int)  # Mapping from items to their supports
    # Count support for every item
    for transaction in transactions:
        for item in transaction:
            items[item] += 1
    # Remove infrequent items
    items = dict((item, support) for item, support in items.items()
        if support >= minimum_support)
    # Build our FP-Tree
    def clean_transaction(transaction):
        # Remove infrequent items and sort by support
        transaction = filter(lambda v: v in items, transaction)
        transaction_list = list(transaction)
        transaction_list.sort(key=lambda v: items[v], reverse=True)
        return transaction_list
    master = FPTree()
    for transaction in map(clean_transaction, transactions):
        master.add(transaction)
    # Helper function to find itemsets with a suffix
    def find_with_suffix(tree, suffix):
        for item, nodes in tree.items():
            support = sum(n.count for n in nodes)
            if support >= minimum_support and item not in suffix:
                # Found frequent itemset
                found_set = [item] + suffix
                yield (found_set, support)
                # Build a conditional tree and recursively search for frequent itemsets within
                cond_tree = tree.conditional_tree_from_paths(tree.prefix_paths(item))
                for s in find_with_suffix(cond_tree, found_set):
                    yield s
    # Start the mining operation
    for itemset in find_with_suffix(master, []):
        yield itemset

class FPTree(object):
    Route = namedtuple('Route', 'head tail')
    def __init__(self):
        self._root = Node(None, None, None, {})
        self._routes = {}
    @property
    def root(self):
        return self._root
    def add(self, transaction):
        point = self._root
        for item in transaction:
            next_point = point.children.get(item)
            if next_point:
                # Increment the count of an existing node
                point.children[item] = next_point.increment()
            else:
                # Add a new node to the tree
                next_point = Node(item, 1, point, {})
                point.children[item] = next_point
                # Link it to the nodes of the same item
                self._update_route(next_point)
            point = next_point
    def _update_route(self, point):
        """Add a node to the route through all nodes of a certain item"""
        current = self._routes.get(point.value)
        if current is None:
            self._routes[point.value] = self.Route(point, point)
        else:
            self._routes[point.value] = self.Route(current.head, point)
            current.tail.children[None] = point