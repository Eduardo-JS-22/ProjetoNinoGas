'use strict';
const {
  Model
} = require('sequelize');
module.exports = (sequelize, DataTypes) => {
  class Cliente extends Model {
    static associate(models) {
      Cliente.hasMany(models.Cobranca, {
        foreignKey: 'cliente_id'
      });
    }
  }
  Cliente.init({
    nome: DataTypes.STRING,
    endereco: DataTypes.STRING,
    telefone: DataTypes.STRING,
    nota: DataTypes.INTEGER
  }, {
    sequelize,
    modelName: 'Cliente',
    tableName: 'clientes',
    paranoid: true
  });
  return Cliente;
};