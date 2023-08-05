import aioredis

from aioredisgraph.util import random_string, quote_string, stringify_param_value
from aioredisgraph.query_result import QueryResult
from aioredisgraph.exceptions import VersionMismatchException
from aioredisgraph.execution_plan import ExecutionPlan

class Graph:
    """
    Graph, collection of nodes and edges.
    """

    def __init__(self, name, from_url=None, host='localhost', port=6379, user=None, password=None):
        """
        Create a new graph.

        Args:
            name: string that represents the name of the graph
            from_url: URL of Redis database
        """
        self.name = name                 # Graph key
        if from_url is not None:
            self.connection_pool = aioredis.ConnectionPool.from_url(from_url)
        else:
            self.connection_pool = aioredis.ConnectionPool.from_url(f'redis://{user}:{password}@{host}:{port}')

        self.nodes = {}
        self.edges = []
        self._labels = []                # List of node labels.
        self._properties = []            # List of properties.
        self._relationshipTypes = []     # List of relation types.
        self.version = 0                 # Graph version

    async def execute_command(self, *args, **kwargs):
        """
        Replace 'self.redis_con.execute_command' from aioredisgraph-py
        All other changes stand for compatibility
        """
        try:
            connection = await self.connection_pool.get_connection(None)  # Param command_name is useless
            await connection.send_command(*args, **kwargs)
            response = await connection.read_response()
            await self.connection_pool.release(connection)
            return response
        except ConnectionError:
            # Todo: What should I do if no connection is available ?
            raise

    def _clear_schema(self):
        self._labels = []
        self._properties = []
        self._relationshipTypes = []

    async def _refresh_schema(self):
        self._clear_schema()
        await self._refresh_labels()
        await self._refresh_relations()
        await self._refresh_attributes()

    async def _refresh_labels(self):
        lbls = await self.labels()

        # Unpack data.
        self._labels = [None] * len(lbls)
        for i, l in enumerate(lbls):
            self._labels[i] = l[0]

    async def _refresh_relations(self):
        rels = await self.relationshipTypes()

        # Unpack data.
        self._relationshipTypes = [None] * len(rels)
        for i, r in enumerate(rels):
            self._relationshipTypes[i] = r[0]

    async def _refresh_attributes(self):
        props = await self.propertyKeys()

        # Unpack data.
        self._properties = [None] * len(props)
        for i, p in enumerate(props):
            self._properties[i] = p[0]

    async def get_label(self, idx):
        """
        Returns a label by it's index

        Args:
            idx: The index of the label
        """
        try:
            label = self._labels[idx]
        except IndexError:
            # Refresh labels.
            await self._refresh_labels()
            label = self._labels[idx]
        return label

    async def get_relation(self, idx):
        """
        Returns a relationship type by it's index

        Args:
            idx: The index of the relation
        """
        try:
            relationshipType = self._relationshipTypes[idx]
        except IndexError:
            # Refresh relationship types.
            await self._refresh_relations()
            relationshipType = self._relationshipTypes[idx]
        return relationshipType

    async def get_property(self, idx):
        """
        Returns a property by it's index

        Args:
            idx: The index of the property
        """
        try:
            propertie = self._properties[idx]
        except IndexError:
            # Refresh properties.
            await self._refresh_attributes()
            propertie = self._properties[idx]
        return propertie

    def add_node(self, node):
        """
        Adds a node to the graph.
        """
        if node.alias is None:
            node.alias = random_string()
        self.nodes[node.alias] = node

    def add_edge(self, edge):
        """
        Adds an edge to the graph.
        """
        if not (self.nodes[edge.src_node.alias]
                and self.nodes[edge.dest_node.alias]):
            raise AssertionError("Both edge's end must be in the graph")

        self.edges.append(edge)

    async def commit(self):
        """
        Create entire graph.
        """
        if len(self.nodes) == 0 and len(self.edges) == 0:
            return None

        query = 'CREATE '
        for _, node in self.nodes.items():
            query += str(node) + ','

        query += ','.join([str(edge) for edge in self.edges])

        # Discard leading comma.
        if query[-1] == ',':
            query = query[:-1]

        return await self.query(query)

    async def flush(self):
        """
        Commit the graph and reset the edges and nodes to zero length
        """
        await self.commit()
        self.nodes = {}
        self.edges = []

    @staticmethod
    def _build_params_header(params):
        if not isinstance(params, dict):
            raise TypeError("'params' must be a dict")
        # Header starts with "CYPHER"
        params_header = "CYPHER "
        for key, value in params.items():
            params_header += str(key) + "=" + stringify_param_value(value) + " "
        return params_header

    async def query(self, q, params=None, timeout=None, read_only=False):
        """
        Executes a query against the graph.

        Args:
            q: the query
            params: query parameters
            timeout: maximum runtime for read queries in milliseconds
            read_only: executes a readonly query if set to True
        """

        # maintain original 'q'
        query = q

        # handle query parameters
        if params is not None:
            query = self._build_params_header(params) + query

        # construct query command
        # ask for compact result-set format
        # specify known graph version
        cmd = "GRAPH.RO_QUERY" if read_only else "GRAPH.QUERY"
        # command = [cmd, self.name, query, "--compact", "version", self.version]
        command = [cmd, self.name, query, "--compact"]

        # include timeout is specified
        if timeout:
            if not isinstance(timeout, int):
                raise Exception("Timeout argument must be a positive integer")
            command += ["timeout", timeout]

        # issue query
        try:
            response = await self.execute_command(*command)
            return await QueryResult.read_response(self, response)
        except aioredis.exceptions.ResponseError as e:
            if "wrong number of arguments" in str(e):
                print("Note: RedisGraph Python requires server version 2.2.8 or above")
            if "unknown command" in str(e) and read_only:
                # `GRAPH.RO_QUERY` is unavailable in older versions.
                return await self.query(q, params, timeout, read_only=False)
            raise e
        except VersionMismatchException as e:
            # client view over the graph schema is out of sync
            # set client version and refresh local schema
            self.version = e.version
            await self._refresh_schema()
            # re-issue query
            return await self.query(q, params, timeout, read_only)

    async def execution_plan(self, query, params=None):
        """
        Get the execution plan for given query,
        GRAPH.EXPLAIN returns an array of operations.

        Args:
            query: the query that will be executed
            params: query parameters
        """
        if params is not None:
            query = self._build_params_header(params) + query

        plan = await self.execute_command("GRAPH.EXPLAIN", self.name, query)
        return "\n".join(plan)

    async def explain(self, query, params=None):
        """
        Get the execution plan for given query,
        GRAPH.EXPLAIN returns ExecutionPlan object.

        Args:
            query: the query that will be executed
            params: query parameters
        """
        if params is not None:
            query = self._build_params_header(params) + query

        plan = await self.execute_command("GRAPH.EXPLAIN", self.name, query)
        return ExecutionPlan(plan)

    async def profile(self, query, params=None):
        """
        Get the profield execution plan for given query,
        GRAPH.PROFILE returns ExecutionPlan object.

        Args:
            query: the query that will be executed
            params: query parameters
        """
        if params is not None:
            query = self._build_params_header(params) + query

        plan = await self.execute_command("GRAPH.PROFILE", self.name, query)
        return ExecutionPlan(plan)

    async def delete(self):
        """
        Deletes graph.
        """
        self._clear_schema()
        return await self.execute_command("GRAPH.DELETE", self.name)

    async def merge(self, pattern):
        """
        Merge pattern.
        """

        query = 'MERGE '
        query += str(pattern)

        return await self.query(query)

    # Procedures.
    async def call_procedure(self, procedure, *args, read_only=False, **kwagrs):
        args = [quote_string(arg) for arg in args]
        q = 'CALL %s(%s)' % (procedure, ','.join(args))

        y = kwagrs.get('y', None)
        if y:
            q += ' YIELD %s' % ','.join(y)

        return await self.query(q, read_only=read_only)

    async def labels(self):
        return (await self.call_procedure("db.labels", read_only=True)).result_set

    async def relationshipTypes(self):
        return (await self.call_procedure("db.relationshipTypes", read_only=True)).result_set

    async def propertyKeys(self):
        return (await self.call_procedure("db.propertyKeys", read_only=True)).result_set
