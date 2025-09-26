const { ApolloServer } = require('@apollo/server');
const { startStandaloneServer } = require('@apollo/server/standalone');
const { ApolloGateway, IntrospectAndCompose } = require('@apollo/gateway');

const gateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({
    subgraphs: [
      { name: 'customers', url: 'http://customers:4001/graphql' },
      { name: 'licenses', url: 'http://licenses:4002/graphql' },
      { name: 'access', url: 'http://access:4003/graphql' },
    ],
  }),
});

const server = new ApolloServer({
  gateway,
  introspection: true,
});

startStandaloneServer(server, {
  listen: { port: 4000 },
}).then(({ url }) => {
  console.log(`🚀 Gateway ready at ${url}`);
});