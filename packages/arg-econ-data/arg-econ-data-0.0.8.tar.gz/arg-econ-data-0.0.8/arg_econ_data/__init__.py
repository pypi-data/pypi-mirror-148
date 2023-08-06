class INDECError(Exception):
    pass

class WaveError(Exception):
    pass

class TrimesterError(Exception):
    pass

class YearError(Exception):
    pass

class AdvertenciaINDEC(Warning):
    pass


class EPH():

    @staticmethod
    def get_microdata(year, trimester_or_wave, type='hogar', advertencias=True, download=False):
        """Genera un DataFrame con los microdatos de la EPH.
        Hasta 2018, usa los datos desde la página de Humai (ihum.ai).
        Desde 2019, los descarga desde la página de INDEC (salvo que cambie el formato del nombre de los archivos y links, debería andar para años posteriores, pero se probó hasta 2021)

        Args:
            @year (int): Año de la EPH
            @trimester_or_wave (int): Trimestre (si año >= 2003) u onda (si año < 2003)
            @type (str, optional): Tipo de base (hogar o individual). Default: 'hogar'.
            @advertencias (bool, optional): Mostrar advertencias metodológicas de INDEC. Defaults to True.
            @download (bool, optional): Descargar los csv de las EPH (en vez de cargarlos directamente a la RAM). Defaults to False.

        Returns:
            pandas.DataFrame: DataFrame con los microdatos de la EPH
        """
        
        from zipfile import ZipFile
        from io import BytesIO
        import os
        import wget
        import fnmatch
        import requests
        import pandas as pd
        
        EPH.handle_exceptions_microdata(year, trimester_or_wave, type, advertencias)
        
        if year < 2019:
            if year >= 2003 and trimester_or_wave is not None:
                url = f'https://datasets-humai.s3.amazonaws.com/eph/{type}/base_{type}_{year}T{trimester_or_wave}.csv'
                link = url
            
            elif year < 2003  and trimester_or_wave is not None:
                url = f'https://datasets-humai.s3.amazonaws.com/eph/{type}/base_{type}_{year}O{trimester_or_wave}.csv'
                link = url
            if download:
                filename = url.split('/')[-1]
                
                if os.path.exists(filename):
                    os.remove(filename)
                    
                filename = wget.download(url)
                df = pd.read_csv(filename, low_memory=False, encoding='unicode_escape')
            else:
                df = pd.read_csv(url, low_memory=False, encoding='unicode_escape')
        elif year >= 2019:
            if trimester_or_wave == 1:
                suffix = 'er' 
            elif trimester_or_wave == 2:
                suffix = 'do'
            elif trimester_or_wave == 3:
                suffix = 'er'
            elif trimester_or_wave == 4:
                suffix = 'to'
                
            try:
                query_str = f"https://www.indec.gob.ar/ftp/cuadros/menusuperior/eph/EPH_usu_{trimester_or_wave}_Trim_{year}_txt.zip"
                print('Descomprimiendo...(si tarda mas de 1 min reintentar, seguramente la página de INDEC esté caída)', end='\r')
                r = requests.get(query_str)
                files = ZipFile(BytesIO(r.content))
                link = query_str
            except:
                try:
                    query_str = f'https://www.indec.gob.ar/ftp/cuadros/menusuperior/eph/EPH_usu_{trimester_or_wave}{suffix}_Trim_{year}_txt.zip'
                    print('Descomprimiendo...(si tarda mas de 1 min reintentar, seguramente la página de INDEC esté caída)', flush=True, end='\r')
                    r = requests.get(query_str)
                    files = ZipFile(BytesIO(r.content))
                    link = query_str
                except:
                    try:
                        query_str = f'https://www.indec.gob.ar/ftp/cuadros/menusuperior/eph/EPH_usu_{trimester_or_wave}{suffix}Trim_{year}_txt.zip'
                        print('Descomprimiendo...(si tarda mas de 1 min reintentar, seguramente la página de INDEC esté caída)', flush=True, sep='', end='\r')
                        r = requests.get(query_str)
                        files = ZipFile(BytesIO(r.content))
                        link = query_str
                    except:
                        raise ValueError(f'No se encontró el archivo de microdatos de la EPH para el año {year} y el trimestre {trimester_or_wave}')	
            try:
                df = pd.read_csv(files.open(f"EPH_usu_{trimester_or_wave}{suffix}_Trim_{year}_txt/usu_{type}_T{trimester_or_wave}{str(year)[-2:]}.txt.txt"), delimiter=';')
                print(f'Se descargó la EPH desde {link}')
                return df
            except:
                try:
                    for file in files.namelist():
                        if fnmatch.fnmatch(file, f'*{type}*.txt'):
                            df = pd.read_csv(files.open(file), low_memory=False, delimiter=';')
                            print(f'Se descargó la EPH desde {link}')
                            return df
                except:
                    raise ValueError('No se encontró el archivo de microdatos en la base de INDEC')
        print(f'Se descargó la EPH desde {link}')
        return df

    @staticmethod
    def handle_exceptions_microdata(year, trimester_or_wave, type, advertencias):
        
        import warnings
        
        if not isinstance(year,int):
            raise YearError("El año tiene que ser un numero")
        
        if not isinstance(trimester_or_wave,int) and not isinstance(trimester_or_wave,int) :
            raise TrimesterError("Debe haber trimestre desde 2003 en adelante (1, 2, 3 o 4) \
                            u onda si es antes de 2003 (1 o 2)")
        
        if (isinstance(trimester_or_wave,int) and trimester_or_wave not in [1,2,3,4]) and (year >= 2003):
            raise TrimesterError("Trimestre/Onda inválido (debe ser entre 1 y 4)")
        
        # if (isinstance(trimester_or_wave,int) and trimester_or_wave not in [1,2]) and (year <= 2003):
        #     raise WaveError("Onda inválida (debe ser 1 o 2)")
        
        if type not in ['individual','hogar']:
            raise TypeError("Seleccione un tipo de base válido: individual u hogar")
        
        if year==2007 and trimester_or_wave==3:
            raise INDECError("\nLa informacion correspondiente al tercer trimestre \
    2007 no está disponible ya que los aglomerados Mar del Plata-Batan, \
    Bahia Blanca-Cerri y Gran La Plata no fueron relevados por causas \
    de orden administrativo, mientras que los datos correspondientes al \
    Aglomerado Gran Buenos Aires no fueron relevados por paro del \
    personal de la EPH")
            
        if (year == 2015 and trimester_or_wave in [3,4]) |  (year ==2016 and trimester_or_wave==3):
            raise INDECError("En el marco de la emergencia estadistica, el INDEC no publicó la base solicitada. \
                    mas información en: https://www.indec.gob.ar/ftp/cuadros/sociedad/anexo_informe_eph_23_08_16.pdf")
        
        if (year == 2003 and trimester_or_wave in [1, 2]):
            raise INDECError('Debido al cambio metodológico en la EPH, en 2003 solo se realizó la encuesta para el 3er y 4to trimestre')
        
        if advertencias:
            if year >= 2007 and year <= 2015:
                warnings.warn('''\n
    Las series estadisticas publicadas con posterioridad a enero 2007 y hasta diciembre \
    2015 deben ser consideradas con reservas, excepto las que ya hayan sido revisadas en \
    2016 y su difusion lo consigne expresamente. El INDEC, en el marco de las atribuciones \
    conferidas por los decretos 181/15 y 55/16, dispuso las investigaciones requeridas para \
    establecer la regularidad de procedimientos de obtencion de datos, su procesamiento, \
    elaboracion de indicadores y difusion.
    Más información en: https://www.indec.gob.ar/ftp/cuadros/sociedad/anexo_informe_eph_23_08_16.pdf 
    (Se puede desactivar este mensaje con advertencias=False)\n-------------------------------------------------------------------------------------------------'''
    , AdvertenciaINDEC, stacklevel=3)


class ENGHo():

    @staticmethod
    def get_microdata(year, type, region=False, download=False):
        
        import pandas as pd
        import zipfile
        
        
        year = ENGHo.handle_exceptions_engho(year, type, region)
        
        
        if year != 1997:
            df = pd.read_table(f'https://github.com/lucas-abbate/engho/blob/main/engho/engho{year}_{type}.zip?raw=true', low_memory=False, compression='zip', sep='|', encoding='latin-1')
            link = f'https://github.com/lucas-abbate/engho/blob/main/engho/engho{year}_{type}.zip'
            print(f'Se descargó la ENGHo desde {link} (bases oficiales de INDEC, actualizadas al 27/4/22)')
            return df
        elif year == 1997:
            df = pd.read_table(f'https://github.com/lucas-abbate/engho/blob/main/engho/engho{year}_{region}_{type}.zip?raw=true', compression='zip', sep='|', encoding='latin-1', header=None)
            link = f'https://github.com/lucas-abbate/engho/blob/main/engho/engho{year}_{region}_{type}.zip'
            print(f'Se descargó la ENGHo desde {link} (bases oficiales de INDEC, actualizadas al 27/4/22)')
            return df
        
    @staticmethod
    def handle_exceptions_engho(year, type, region):
        import warnings
        
        if year in [2017, 2018, 17, 18, '17-18', '17/18', '2017/2018', '2017-2018']:
            year = 2018
        elif year in [2012, 2013, 12, 13, '12-13', '12/13', '2012-2013', '2012/2012']: 
            year = 2012
        elif year in [2004, 2005, 4, 5, '04-05', '04/05', '2004-2005', '2004/2005']:
            year = 2005
        elif year in [1996, 1997, 96, 97, '96-97', '96/97', '1996/1997', '1996-1997']:
            year = 1997
            if region not in ['metropolitana', 'cuyo', 'noreste', 'noroeste', 'pampeana']:
                raise TypeError('La ENGHo 96-97 está publicada por regiones para: metropolitana, cuyo, noreste, noroeste y pampeana')
            link_variables = 'https://www.indec.gob.ar/ftp/cuadros/menusuperior/engho/engh9697_dise%C3%B1o_registro.zip'
            warnings.warn(f'Los archivos de ENGHo 96-97 proporcionados por INDEC no tienen nombres de variable. Se pueden consultar para cada base en {link_variables}', AdvertenciaINDEC, stacklevel=3)
        elif year in [1985, 1986, 85, 86, '85-86', '85/86', '1985-1986', '1985/1986']:
            year = 1986
        else:
            raise YearError("La ENGHo solo se realizó en 17-18, 12-13, 04-05, 96-97 y 85-86. Usar alguno de esos años")

        if year != 1997 and region != False:
            warnings.warn('La única base regionalizada es la de 96-97 (y la 85-86, solo para CABA y conurbano). Se omitirá la region', AdvertenciaINDEC, stacklevel=3)
        

        if year == 2018 and type not in ['personas', 'hogares', 'equipamiento', 'gastos', 'habitos']:
            raise TypeError('En la ENGHo 17-18, las bases son: personas, hogares, equipamiento, gastos y habitos')
        
        elif year == 2012 and type not in ['personas', 'hogares', 'equipamiento', 'gastos', 'ingresos', 'gtnfp']:
            raise TypeError('En la ENGHo 12-13, las bases son: personas, hogares, equipamiento, gastos y gtnfp (gastos segun tipo de negocio y forma de pago)')
        
        elif year == 2005 and type not in ['personas', 'hogares', 'equipamiento', 'gastos', 'ingresos', 'gtnfp']:
            raise TypeError('En la ENGHo 04-05, las bases son: personas, hogares, equipamiento, gastos, ingresos y gtnfp (gastos segun tipo de negocio y forma de pago)')
        
        elif year == 1997 and type not in ['personas', 'hogares', 'equipamiento', 'ingresos', 'gastos', 'gtnfp', 'cantidades']:
            raise TypeError('En la ENGHo 96-97, las bases son: personas, hogares, equipamiento, gastos, cantidades, ingresos y gtnfp (gastos segun tipo de negocio y forma de pago)')
        
        elif year == 1986 and type not in ['personas', 'hogares', 'articulo', 'ingresos', 'capitulo', 'gastos', 'grupo']:
            raise TypeError('En la ENGHo 85-86, las bases son: personas, hogares, articulo, gastos, ingresos, capitulo y grupo')
        
        return year    
    
    
eph = EPH
ENGHO = ENGHo
engho = ENGHo



class Series():

    @staticmethod
    def get_metadata(organizacion=False):
        '''
        Devuelve las series disponibles para descargar.
        Son alrededor de 32k, así que '''
        
        import pandas as pd
        if organizacion:
            df = pd.read_csv(f'https://apis.datos.gob.ar/series/api/dump/{organizacion}/series-tiempo-metadatos.csv')
        else:
            df = pd.read_csv('https://apis.datos.gob.ar/series/api/dump/series-tiempo-metadatos.csv')
        return df
    
    @staticmethod
    def search(texto, **kwargs):
        import requests
        import urllib.parse
        API_BASE_URL = "https://apis.datos.gob.ar/series/api/search"
        kwargs["ids"] = ",".join(ids)
        return "{}{}?{}".format(API_BASE_URL, "series", urllib.parse.urlencode(kwargs))


    @staticmethod
    def get_sources(organizacion=False):
        import pandas as pd
        if organizacion:
            df = pd.read_csv(f'https://apis.datos.gob.ar/series/api/dump/{organizacion}/series-tiempo-fuentes.csv')
        else:
            df = pd.read_csv('https://apis.datos.gob.ar/series/api/dump/series-tiempo-fuentes.csv')
        return df

    @staticmethod
    def get_api_call(ids, **kwargs):
        import urllib.parse
        API_BASE_URL = "https://apis.datos.gob.ar/series/api/"
        try:
            kwargs["ids"] = ",".join(ids)
        except TypeError:
            query = ''
            n = 1
            for id in ids[0]:
                print(id)
                query += id
                n+=1
                if n == len(ids[0]):
                    query += ','
            kwargs['ids'] = query
                
        return "{}{}?{}".format(API_BASE_URL, "series", urllib.parse.urlencode(kwargs))

    @staticmethod
    def get_microdata(serie_id, **kwargs):
        
        import pandas as pd
        querys = Series.get_api_call([serie_id], format='csv', **kwargs)
        print(querys)
        df = pd.read_csv(querys)
        return df