const FOTO = "https://example.com/mascota.jpg";

function mascota(id, name, status) {
  return {
    id,
    name,
    photoUrls: [FOTO],
    status,
  };
}

function guardar(nombre, payload) {
  return cy.writeFile(`reports/evidencia/${nombre}.json`, payload, { log: false });
}

function buscarPorEstado(petId, intento) {
  return cy
    .request({
      method: "GET",
      url: "/pet/findByStatus",
      qs: { status: "sold" },
      headers: { Accept: "application/json" },
      timeout: 60000,
    })
    .then((response) => {
      const lista = Array.isArray(response.body) ? response.body : [];
      const mia = lista.find((item) => item.id === petId);
      if (mia || intento >= 3) {
        return { response, lista, mia, intento };
      }
      return cy.wait(2000).then(() => buscarPorEstado(petId, intento + 1));
    });
}

describe("PetStore: ciclo de una mascota", () => {
  const petId = Math.floor(100000000 + Math.random() * 900000000);
  const nombreInicial = `Mascota-${petId}`;
  const nombreVendido = `Mascota-vendida-${petId}`;

  after(() => {
    cy.request({
      method: "DELETE",
      url: `/pet/${petId}`,
      failOnStatusCode: false,
    });
  });

  it("CP-01 añade una mascota a la tienda", () => {
    const entrada = mascota(petId, nombreInicial, "available");
    cy.request({
      method: "POST",
      url: "/pet",
      headers: { Accept: "application/json" },
      body: entrada,
    }).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body.id).to.eq(petId);
      expect(response.body.name).to.eq(nombreInicial);
      expect(response.body.status).to.eq("available");
      return guardar("01-alta", {
        caso: "CP-01 Añadir una mascota",
        metodo: "POST /v2/pet",
        entrada,
        http: response.status,
        duracionMs: response.duration,
        salida: response.body,
      });
    });
  });

  it("CP-02 consulta la mascota por id", () => {
    cy.request({
      method: "GET",
      url: `/pet/${petId}`,
      headers: { Accept: "application/json" },
    }).then((response) => {
      expect(response.status).to.eq(200);
      expect(response.body.id).to.eq(petId);
      expect(response.body.name).to.eq(nombreInicial);
      expect(response.body.status).to.eq("available");
      return guardar("02-consulta-por-id", {
        caso: "CP-02 Consulta por id",
        metodo: `GET /v2/pet/${petId}`,
        http: response.status,
        duracionMs: response.duration,
        salida: response.body,
      });
    });
  });

  it("CP-03 actualiza el nombre y el estado a sold", () => {
    const entrada = mascota(petId, nombreVendido, "sold");
    let actualizacion;
    cy.request({
      method: "PUT",
      url: "/pet",
      headers: { Accept: "application/json" },
      body: entrada,
    })
      .then((response) => {
        expect(response.status).to.eq(200);
        expect(response.body.id).to.eq(petId);
        expect(response.body.name).to.eq(nombreVendido);
        expect(response.body.status).to.eq("sold");
        actualizacion = response;
        return cy.request({
          method: "GET",
          url: `/pet/${petId}`,
          headers: { Accept: "application/json" },
        });
      })
      .then((consulta) => {
        expect(consulta.status).to.eq(200);
        expect(consulta.body.name).to.eq(nombreVendido);
        expect(consulta.body.status).to.eq("sold");
        return guardar("03-actualizacion", {
          caso: "CP-03 Actualizar nombre y estado sold",
          metodo: "PUT /v2/pet y GET /v2/pet/{id}",
          entrada,
          httpPut: actualizacion.status,
          httpGet: consulta.status,
          duracionMs: consulta.duration,
          salida: consulta.body,
        });
      });
  });

  it("CP-04 consulta la mascota modificada por estado sold", () => {
    buscarPorEstado(petId, 1).then(({ response, lista, mia, intento }) => {
      expect(response.status).to.eq(200);
      expect(lista, "findByStatus debe devolver una lista").to.be.an("array");
      expect(mia, `no apareció la mascota ${petId} con estado sold`).to.exist;
      expect(mia.name).to.eq(nombreVendido);
      expect(mia.status).to.eq("sold");
      return guardar("04-busqueda-por-estado", {
        caso: "CP-04 Búsqueda por estado sold",
        metodo: "GET /v2/pet/findByStatus?status=sold",
        http: response.status,
        duracionMs: response.duration,
        intentos: intento,
        totalEnLaLista: lista.length,
        mascotaEncontrada: {
          id: mia.id,
          name: mia.name,
          status: mia.status,
        },
      });
    });
  });

  it("CP-05 un id que no existe responde 404", () => {
    const idInexistente = 404404404;
    cy.request({
      method: "GET",
      url: `/pet/${idInexistente}`,
      headers: { Accept: "application/json" },
      failOnStatusCode: false,
    }).then((response) => {
      expect(response.status).to.eq(404);
      return guardar("05-id-inexistente", {
        caso: "CP-05 Id inexistente",
        metodo: `GET /v2/pet/${idInexistente}`,
        http: response.status,
        duracionMs: response.duration,
        salida: response.body,
      });
    });
  });
});
