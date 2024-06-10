'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class Cobranca extends Model {
    static associate(models) {
      Cobranca.belongsTo(models.Cliente, {
        foreignKey: 'cliente_id'
      });
    }
  }
  Cobranca.init({
    dataVenda: DataTypes.DATEONLY,
    valor_total: DataTypes.FLOAT,
    ativo: DataTypes.BOOLEAN,
    data_fechamento: DataTypes.DATEONLY
  }, {
    sequelize,
    modelName: 'Cobranca',
    tableName: 'cobrancas',
    paranoid: true
  });
  return Cobranca;
};