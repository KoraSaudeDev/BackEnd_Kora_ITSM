from flask import Blueprint, jsonify, request
from hdbcli import dbapi
from app.sap_connection import ConnectionSAPHANA

sap_blueprint = Blueprint('sap', __name__)

@sap_blueprint.route('/material', methods=['GET'])
def get_material():
    material = request.args.get('material', '')
    tipo = request.args.get('tipo', '')
    grupo = request.args.get('grupo', '')

    if not material:
        return jsonify({"error": "Parâmetro 'material' é obrigatório"}), 400
    if not tipo:
        return jsonify({"error": "Parâmetro 'tipo' é obrigatório"}), 400
    if not grupo:
        return jsonify({"error": "Parâmetro 'grupo' é obrigatório"}), 400
    
    connection = ConnectionSAPHANA()
    if not connection:
        return jsonify({"error": "Não foi possível conectar ao SAP HANA"}), 500
    
    try:
        cursor = connection.cursor()
        
        base_query = """
            SELECT DISTINCT MA.MATNR, MA.MAKTX, AVG(MB.VERPR), MR.MATKL, MR.MEINS
            FROM SAPHANADB.MAKT MA
            JOIN SAPHANADB.MBEW MB ON MA.MATNR = MB.MATNR
            JOIN SAPHANADB.MARA MR ON MA.MATNR = MR.MATNR
            WHERE MA.MAKTX LIKE ? AND MR.MATKL LIKE ?
        """
        params = [f"%{material.upper()}%", f"%{grupo.upper()}%"]
        
        if tipo == "Produto":
            base_query += " AND MR.MTART <> 'SERV'"
        elif tipo == "Serviço":
            base_query += " AND MR.MTART = 'SERV'"
        
        base_query += " GROUP BY MA.MATNR, MA.MAKTX, MR.MATKL, MR.MEINS LIMIT 40"
        
        cursor.execute(base_query, params)
        materials = cursor.fetchall()

        cursor.close()
        connection.close()

        material_list = [{"codigo": row[0], "material": row[1], "preco": row[2], "grupo": row[3], "unidadeMedida": row[4]} for row in materials]

        return jsonify(material_list)
    except dbapi.Error as e:
        print(f"Erro ao executar query: {e}")
        return jsonify({"error": "Erro ao buscar materiais"}), 500

@sap_blueprint.route('/grupo-mercadoria', methods=['GET'])
def get_grupo_mercadoria():
    connection = ConnectionSAPHANA()
    if not connection:
        return jsonify({"error": "Não foi possível conectar ao SAP HANA"}), 500
    
    try:
        cursor = connection.cursor()
        
        query = """
            SELECT MATKL FROM SAPHANADB.T023 WHERE BKLAS <> '' AND BKLAS IS NOT NULL ORDER BY MATKL ASC
        """
        
        cursor.execute(query)
        retorno = cursor.fetchall()

        cursor.close()
        connection.close()

        result = [row[0] for row in retorno]

        return jsonify(result)
    except dbapi.Error as e:
        print(f"Erro ao executar query: {e}")
        return jsonify({"error": "Erro ao buscar grupos de mercadorias"}), 500

@sap_blueprint.route('/centro-custo', methods=['GET'])
def get_centro_custo():
    empresa = request.args.get('empresa', '')

    if not empresa:
        return jsonify({"error": "Parâmetro 'empresa' é obrigatório"}), 400
    
    if not empresa.isdigit():
        return jsonify({"error": "Parâmetro 'empresa' deve conter apenas números"}), 400
    
    connection = ConnectionSAPHANA()
    if not connection:
        return jsonify({"error": "Não foi possível conectar ao SAP HANA"}), 500
    
    try:
        cursor = connection.cursor()
        
        query = """
            SELECT DISTINCT csk.KOSTL, cst.LTEXT FROM SAPHANADB.CSKS csk JOIN SAPHANADB.CSKT cst ON csk.KOSTL = cst.KOSTL WHERE csk.BUKRS = ? ORDER BY cst.LTEXT
        """
        
        cursor.execute(query, (empresa,))
        retorno = cursor.fetchall()

        cursor.close()
        connection.close()

        result = [{"codigo": row[0], "descricao": row[1], "centro_custo": f"{row[1]} ({row[0]})"} for row in retorno]

        return jsonify(result)
    except dbapi.Error as e:
        print(f"Erro ao executar query: {e}")
        return jsonify({"error": "Erro ao buscar centros de custos"}), 500
    
@sap_blueprint.route('/fornecedor', methods=['GET'])
def get_fornecedor():
    fornecedor = request.args.get('fornecedor', '')
    
    connection = ConnectionSAPHANA()
    if not connection:
        return jsonify({"error": "Não foi possível conectar ao SAP HANA"}), 500
    
    try:
        cursor = connection.cursor()
        
        if not fornecedor:
            query = f"""SELECT DISTINCT lfa.LIFNR, lfa.NAME1  FROM SAPHANADB.LFA1 lfa LIMIT 40"""
        else:
            query = f"""SELECT DISTINCT lfa.LIFNR, lfa.NAME1  FROM SAPHANADB.LFA1 lfa WHERE lfa.NAME1 LIKE '%{fornecedor.upper()}%' LIMIT 40"""
        
        cursor.execute(query)
        retorno = cursor.fetchall()

        cursor.close()
        connection.close()

        result = [{"codigo": row[0], "fornecedor": row[1]} for row in retorno]

        return jsonify(result)
    except dbapi.Error as e:
        print(f"Erro ao executar query: {e}")
        return jsonify({"error": "Erro ao buscar fornecedores"}), 500