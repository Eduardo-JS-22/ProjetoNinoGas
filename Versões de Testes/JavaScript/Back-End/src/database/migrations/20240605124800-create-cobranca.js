'use strict';
/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface, Sequelize) {
    await queryInterface.createTable('Cobrancas', {
      id: {
        allowNull: false,
        autoIncrement: true,
        primaryKey: true,
        type: Sequelize.INTEGER
      },
      cliente: {
        type: Sequelize.STRING
      },
      dataVenda: {
        type: Sequelize.DATEONLY
      },
      valorTotal: {
        type: Sequelize.FLOAT
      },
      ativo: {
        type: Sequelize.BOOLEAN
      },
      dataFechamento: {
        type: Sequelize.DATEONLY
      },
      createdAt: {
        allowNull: false,
        type: Sequelize.DATE
      },
      updatedAt: {
        allowNull: false,
        type: Sequelize.DATE
      }
    });
  },
  async down(queryInterface, Sequelize) {
    await queryInterface.dropTable('Cobrancas');
  }
};