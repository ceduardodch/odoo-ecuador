# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api, _

class Ficha(models.Model):
    _name = 'seguridad.ficha'
    _description = "Employee"
    name = fields.Many2one('hr.employee', string="Empleado", required = True)
    identificacion = fields.Char( string="Identificación:",related='name.identification_id',  readonly=True, store = True,)
    dob = fields.Date(string="Fecha de Nacimiento:",related='name.birthday', readonly=True, )
    age = fields.Char(string="Edad:",compute='_set_imc', readonly=True, store = True, )
    area = fields.Char(string="Área de Trabajo:", related='name.department_id.name', readonly=True, store = True,)
    job = fields.Char(string="Puesto de Trabajo:", related='name.job_id.name', readonly=True,store = True,)
    marital = fields.Selection(string="Estado Civil:", related='name.marital', readonly=True)

    #def get_age(self):
    @api.onchange('dob')
    def get_age(self):
        res = {}
        if self.dob:
            dob = datetime.strptime(self.dob, "%Y-%m-%d")
            age_calc = (datetime.today() - dob).days / 365
            age = str(age_calc) + ' Años'
            self.age = age

    tipo = fields.Selection(string="Tipo de Ficha", selection=[('ingreso', 'Ingreso'), ('desvinculacion', 'Desvinculación')], required = True)
    antecedente_ids = fields.One2many('seguridad.antecedente', 'ficha_id', string="Ingrese los antecedentes laborales")
    factor_ids = fields.One2many('seguridad.factor', 'ficha_id',string="Ingrese los factores de riesgo")
    sistema_id= fields.Many2many('seguridad.sistema', string="Órgano o Sistema")
    observacion = fields.Text(string="Observaciones")
    presion = fields.Integer(string="Presión Arterial")
    frecuencia = fields.Integer(string="Frecuencia Cardíaca")
    peso = fields.Float(digits=(6, 2), string="Peso (Kg)")
    estatura = fields.Float(digits=(6, 2), string="Estatura(mts)")
    imc =fields.Float(string=_("IMC (kg/mts2)"),compute='_set_imc', store = True)
    lateralidad = fields.Selection(string="Lateralidad", selection=[('diestra', 'Diestra'), ('zurda', 'Zurda'),('ambidiestro', 'Ambidiestro')])
    perimetro = fields.Integer(string="Perimetro Abdominal", required=False)
    organo_ids = fields.One2many('seguridad.organo', 'ficha_id' )
    resultado_ids= fields.One2many('seguridad.resultado', 'ficha_id')
    resultado_complementario_ids = fields.One2many('seguridad.resultado_complementario', 'ficha_id')
    diagnostico_ids = fields.One2many('seguridad.diagnostico', 'ficha_id')
    condicion = fields.Selection(string="Condición", selection=[('apto', 'Apto'), ('noapto', 'No Apto'),
                                                                    ('restricciones', 'Apto con Restricciones')])
    vacuna_ids = fields.One2many('seguridad.vacuna', 'ficha_id')
    observacion_condicion = fields.Text(string="Observaciones")
    familiar_ids=fields.One2many('seguridad.antecedente_familiar', 'ficha_id')
    personal_ids = fields.One2many('seguridad.antecedente_personal', 'ficha_id')
    @api.depends('peso')
    def _set_imc(self):
        for r in self:
            if  r.estatura != 0:
                r.imc = r.peso / (r.estatura*r.estatura)




    hoja_count = fields.Integer(compute='_compute_hoja_count', string='Hoja Evolución')
    def _compute_hoja_count(self):
        self.hoja_count = self.env['seguridad.hoja_evolucion'].search_count([('name', '=', self.id)])
    hoja_ids = fields.One2many('seguridad.hoja_evolucion', 'name')

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name,tipo)',
         "La ficha debe ser única por empleado y tipo"),
        ]
    habito_ids = fields.One2many('seguridad.habito', 'ficha_id')


class Vacuna(models.Model):
    _name = 'seguridad.vacuna'

    name = fields.Many2one(comodel_name="seguridad.tipo_vacuna", string="Tipo de Vacuna", required=True, )
    fecha = fields.Date(string = "Fecha de Vacunación")
    ficha_id = fields.Many2one('seguridad.ficha', string="Ficha")

class TipoVacuna(models.Model):
    _name = 'seguridad.tipo_vacuna'
    name = fields.Char(string="Tipo de Vacuna")


class Antecedentes(models.Model):
    _name = 'seguridad.antecedente'
    name = fields.Char(string="Institución Anterior", required=True)
    cargo = fields.Text(string="Descripción de las funciones del cargo",)
    funcion = fields.Text(string="Descripción de las funciones o procesos de trabajo peligrosos")
    elemento_id = fields.Many2many('seguridad.elementos_proteccion', string="Elementos de Protección")
    ficha_id = fields.Many2one('seguridad.ficha', string="Ficha")

class Habitos(models.Model):
    _name = 'seguridad.habito'

    name = fields.Selection(string="Hábitos", selection=[('alcohol', 'Alcohol'), ('cigarrillo', 'Cigarrillo/Tabaco/Pipa'),('sustancias', 'Sustancias Psicoantivas'),('actividad', 'Actividad Física')])
    description = fields.Text(string="Descripción",)
    ficha_id = fields.Many2one('seguridad.ficha', string="Ficha")

class AntecedentesFamiliar(models.Model):
    _name = 'seguridad.antecedente_familiar'
    name = fields.Selection(string="Antecedente", selection=[('primer', 'Primer Grado de Consanguinidad'), ('asma', 'Asma'),
                                                             ('cancer', 'Cáncer'), ('diabetes', 'Diabetes'), ('enfermendad', 'Enfermedad Coronaria'),
                                                             ('accidente', 'Accidente Cerebro Vascular'), ('hipertension', 'Hipertension Arterial'),
                                                             ('colagenosis', 'Colagenosis'), ('patologias', 'Patologias Tiroideas'),
                                                             ('otros', 'Otros')])
    descripcion = fields.Text(string="Descripción")
    ficha_id = fields.Many2one('seguridad.ficha', string="Ficha")

class AntecedentesPersonal(models.Model):
    _name = 'seguridad.antecedente_personal'
    name = fields.Selection(string="Antecedente", selection=[('primer', 'Clínicos'), ('quirurgicos', 'Quirurgicos')
                                                            , ('gineco', 'Gineco-Obstétricos'), ('farmocolofico', 'Farmocológico/Alergicos'), ('psiquiatricos', 'Psiquiátricos')])
    descripcion = fields.Text(string="Descripción")
    ficha_id = fields.Many2one('seguridad.ficha', string="Ficha")

class Factores(models.Model):
    _name = 'seguridad.factor'
    name = fields.Char(string="Institución o Empresa", required=True)
    cargo = fields.Text(string="Cargos desempeñados")
    anos = fields.Integer(string="Tiempo (Años) de exposición")
    fisico_id = fields.Many2many('seguridad.factor_fisico', string="Físico")
    quimico_id = fields.Many2many('seguridad.factor_quimico', string="Químico")
    ergonomico_id = fields.Many2many('seguridad.factor_ergonomico', string="Ergónomico")
    biologico_id = fields.Many2many('seguridad.factor_biologico', string="Biológico")
    psicologico_id = fields.Many2many('seguridad.factor_psicologico', string="Psicológico")
    ficha_id = fields.Many2one('seguridad.ficha', string="Ficha")

class ElementosProteccion(models.Model):
    _name = 'seguridad.elementos_proteccion'
    name = fields.Char(string="Elementos de Protección", required=True)

class FactoresFisicos(models.Model):
    _name = 'seguridad.factor_fisico'
    name = fields.Char(string="Físico", required=True)

class FactoresQuimicos(models.Model):
    _name = 'seguridad.factor_quimico'
    name = fields.Char(string="Químico", required=True)

class FactoresErgonomicos(models.Model):
    _name = 'seguridad.factor_ergonomico'
    name = fields.Char(string="Ergonómico", required=True)

class FactoresBiologico(models.Model):
    _name = 'seguridad.factor_biologico'
    name = fields.Char(string="Biológico", required=True)

class FactoresPsicosocial(models.Model):
    _name = 'seguridad.factor_psicologico'
    name = fields.Char(string="Psicológico", required=True)

class RevisionSistema(models.Model):
    _name = 'seguridad.sistema'
    name = fields.Char(string="Órgano o Sistema", required=True)

class OrganoObservaciones(models.Model):
    _name = 'seguridad.organo'
    _description = 'Tabla que guarda las observaciones por cada organo'

    organo_id = fields.Many2many('seguridad.sistema',string="Órgano/Sistema")
    tipo = fields.Selection(string="Normal/Anormal", selection=[('normal', 'Normal'), ('anormal', 'Anormal')])
    observacion = fields.Text(string="Observaciones")
    ficha_id = fields.Many2one('seguridad.ficha', string="Ficha")

class Resultado(models.Model):
    _name = 'seguridad.resultado'
    _description = 'Resultados'
    name = fields.Char(string = "Examen", required = True)
    valor = fields.Float(string="Valor")
    observacion = fields.Text(string="Observaciones")
    ficha_id = fields.Many2one('seguridad.ficha', string="Ficha")

class ResultadoComplementario(models.Model):
    _name = 'seguridad.resultado_complementario'
    _description = 'Resultados Complementarios'
    name = fields.Char(string="Examen Complementarios", required=True)
    valor = fields.Float(string="Valor")
    observacion = fields.Text(string="Observaciones")
    ficha_id = fields.Many2one('seguridad.ficha', string="Ficha")

class Diagnostico(models.Model):
    _name = 'seguridad.diagnostico'
    diagnostico = fields.Text(string="Diagnóstico")
    tratamiento = fields.Text(string="Tratamiento")
    observacion =  fields.Text(string="Observación")
    ficha_id = fields.Many2one('seguridad.ficha', string="Ficha")

class HojaEvolucion(models.Model):
    _name = 'seguridad.hoja_evolucion'
    fecha = fields.Datetime(string="Fecha Atención", required = True)
    nota_evolucion = fields.Text(string="Nota de Evolución", required = True)
    prescripcion = fields.Text(string="Prescripción Médica")
    medicamentos =  fields.Text(string="Administración de Medicamentos")
    desde = fields.Date(string="Reposo Desde:")
    hasta = fields.Date(string="Hasta:")
    name = fields.Many2one('seguridad.ficha', string="Empleado")



